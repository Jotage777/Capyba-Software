from datetime import datetime, timedelta, date
from time import time
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, extract, func, or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, url_for
import jwt
from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = 'sqlite:///myapp.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

#Função para consultar a data e a hora
def brazilian_time():
    return datetime.utcnow() - timedelta(hours=3)

#Classe que representa a tabela de usuarios
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(64), primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)  # E-mail
    name = db.Column(db.String(64), nullable=False)  # Nome completo
    password_hash = db.Column(db.String(128), nullable=False)  # Hash da senha
    confirmed = db.Column(db.Boolean, default=False)  # Confirmação do email
    code = db.Column(db.String(5), index=True)  # Codigo de confirmação
    code_expiration = db.Column(db.DateTime)  # Período em que o codigo se expira
    token = db.Column(db.String(240), index=True, unique=True)  # Token de login
    token_expiration = db.Column(db.DateTime)  # Período em que o token se expira
    reset_password_token = db.Column(
        db.String(240), index=True, unique=True, nullable=True
    )  # Refresh token
    reset_password_token_expiration = db.Column(
        db.DateTime, nullable=True
    )  # Período em que o refresh token se expira
    #ForeignKey
    imagens = db.relationship('Imagem', backref='user', lazy=True)

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
            current_app.config.get("USER_SECRET_KEY"),
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
                token, current_app.config.get("USER_SECRET_KEY"), algorithms=["HS256"]
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
            "confirmed":self.confirmed
            
        }

class Imagem(db.Model):
    __tablename__ = 'images'
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