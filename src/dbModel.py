from datetime import datetime, timedelta, date
from time import time
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, extract, func, or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
import jwt
from flask_sqlalchemy import SQLAlchemy
import random
from sqlalchemy.orm import class_mapper

from dotenv import load_dotenv
import os
load_dotenv()

db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = 'sqlite:///myapp.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

#Função para consultar a data e a hora
def brazilian_time():
    return datetime.utcnow() - timedelta(hours=3)


class Permission:
    PUBLIC = 1
    VIP = 2
    ADMIN = 4


#Classe que representa a tabela de usuarios
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)  # E-mail
    name = db.Column(db.String(64), nullable=False)  # Nome completo
    password_hash = db.Column(db.String(128), nullable=False)  # Hash da senha
    cpf = db.Column(db.String(11), unique=True, index=True)  # CPF
    birth_date = db.Column(db.DateTime, index = True)  # Data de nascimento
    phone = db.Column(db.String, unique=True)  # Telefone
    confirmed = db.Column(db.Boolean, default=False)  # Confirmação do email
    code = db.Column(db.String(5), index=True)  # Codigo de confirmação
    code_expiration = db.Column(db.DateTime)  # Período em que o codigo se expira
    token = db.Column(db.String(240), index=True, unique=True)# Token de login
    token_expiration = db.Column(db.DateTime)# Período em que o token se expira
    vip = db.Column(db.Boolean, default=False)# Acesso a area de login privada
    
    #ForeignKey
    imagens = db.relationship('Imagem', backref='user', lazy=True)
    role_id = db.Column(db.Integer, ForeignKey("roles.id"))

    # criando o administrador
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role_id is None:
            if self.email == 'admin@admin.com':
                self.role_id = (
                    Role.query.filter_by(name="ADMINISTRATOR").first().id
                )
            else:
                self.role_id = Role.query.filter_by(default=True).first().id


    @property  # O que acontece quando User.password é chamado
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter  # Criando o hash de senha para a senha digitada pelo usuário
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def change_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):  # Verifique se a senha digitada está correta
        return check_password_hash(self.password_hash, password)

    
    # Gerando o token do usuario
    def generate_token(self):
        now = brazilian_time()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
     
        self.token = jwt.encode(
            {"id": self.id, "time": str(now)},
            os.environ.get('SECRET_KEY'),
            algorithm="HS256",
        )
        self.token_expiration = now + timedelta(seconds=86400)
        db.session.add(self)
        
        return self.token

    # Verificando o token
    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(
                token, os.environ.get('SECRET_KEY'), algorithms=["HS256"]
            )
            user_id = payload["id"]
            user = User.query.get(user_id)
            if user is None or user.token_expiration < brazilian_time():
                return None
            return user
        except Exception as e:
            return None

    # Revoke token
    def revoke_token(self):
        self.token_expiration = brazilian_time() - timedelta(seconds=1)

    #Gerando o codigo de confirmação
    def generateCode(self):
        now = brazilian_time()
        code = str(random.randint(1000, 9999))
        self.code = code
        self.code_expiration = now + timedelta(seconds=600)
        db.session.add(self)
        db.session.commit()
        return code
    
    #Confirmando o codigo de confirmação
    def confirmedCode(self,code):
        if  self is None or self.code_expiration < brazilian_time():
            return False
        
        if code == self.code:
            self.confirmed = True
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False

    def profileDict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "confirmed":self.confirmed,
            "cpf":self.cpf,
            "birth_date": self.birth_date,
            "phone": self.phone,
            
            
        }

class Imagem(db.Model):
    __tablename__ = 'imagens'
    id = db.Column(db.String(64), primary_key=True, index=True)
    name = db.Column(db.String(50), index=True)# Nome do arquivo
    data = db.Column(db.LargeBinary, nullable=False)#Conteudo do arquivo
    user_id = db.Column(db.String(64), ForeignKey('users.id'))# User id correspondente a imagem
    
    def profileDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id":self.user_id
            
        }
    

class Filmes(db.Model):
    __tablename__ = 'filmes'
    id = db.Column(db.String(64), primary_key=True, index=True)
    name = db.Column(db.String(50), index=True)# Nome do filme
    descricao = db.Column(db.String(500), nullable=False)#Descrição do filme
    avaliacao = db.Column(db.Integer, index=True, nullable=False)# Avaliação do filme
    anoLancamento = db.Column(db.Integer, index=True, nullable=False)# ano de lançamento
    
    def profileDictPublic(self):
        return {
            "id": self.id,
            "name": self.name,
            "descrição":self.descricao,
            "avaliação":self.avaliacao,
            "ano de lançamento": self.anoLancamento
            
        }

class Livros(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.String(64), primary_key=True, index=True)
    name = db.Column(db.String(50), index=True)# Nome do livro
    autor = db.Column(db.String(50), nullable=False)#Autor do livro
    avaliacao = db.Column(db.Integer, index=True, nullable=False)# Avaliação do filme
    anoLancamento = db.Column(db.Integer, index=True, nullable=False)# ano de lançamento
    
    def profileDictPublic(self):
        return {
            "id": self.id,
            "name": self.name,
            "Autor":self.autor,
            "avaliação":self.avaliacao,
            "ano de lançamento": self.anoLancamento
            
        }
    
class Series(db.Model):
    __tablename__ = 'series'
    id = db.Column(db.String(64), primary_key=True, index=True)
    name = db.Column(db.String(50), index=True)# Nome do filme
    descricao = db.Column(db.String(500), nullable=False)#Descrição do filme
    avaliacao = db.Column(db.Integer, index=True, nullable=False)# Avaliação do filme
    anoLancamento = db.Column(db.Integer, index=True, nullable=False)# ano de lançamento
    
    def profileDictPublic(self):
        return {
            "id": self.id,
            "name": self.name,
            "descrição":self.descricao,
            "avaliação":self.avaliacao,
            "ano de lançamento": self.anoLancamento
            
        }

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    # If a permission value is None sets it to 0
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            "PUBLIC": [Permission.PUBLIC],
            "VIP": [Permission.PUBLIC, Permission.VIP],
            "ADMINISTRATOR": [Permission.PUBLIC, Permission.VIP, Permission.ADMIN],
        }
        default_role = "PUBLIC"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            # Insert permissions
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = role.name == default_role
            db.session.add(role)
        db.session.commit()

#Função para transformar o response dos filtros de pesquisas em Json serializable
def to_dict(model):
    """Converte um objeto SQLAlchemy em um dicionário Python."""
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)
