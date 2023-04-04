import uuid
from flask import Blueprint, request, jsonify,g
from dbModel import db, User, Imagem
from sqlalchemy import exists
from configEmail import send_email
from datetime import datetime
from decorators import is_valid_token
from validarCpf import validar_cpf

from dotenv import load_dotenv
import os
load_dotenv()

teste = os.environ.get('TESTING')
print(teste)
user = Blueprint('user', __name__)

#Rota para registrar um usuario
@user.route('/register', methods=['POST'])
def registerUser():
    
    #Imagem, name, email e password fornecidos pela requisição
    imagem = request.files['imagem']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    # Checar se todos os dados foram fornecidos
    if not (
        (
            name
            and email
            and password
            and imagem
        )
    ):
        return jsonify({"message": "É preciso fornecer E-mail, Nome, Senha e Imagem"}), 400
    
    # Verificar se já existe um usuário com este email
    email_exists = db.session.query(
        exists().where((User.email == email))
    ).scalar()

    if email_exists:
        return jsonify({"message": "E-mail já cadastrado"}), 400
    
    #Criando objeto user
    user = User(
        id = str(uuid.uuid4()),
        email = email,
        name = name,
        password = password
    )
    #Criando objeto imagem
    imagemObject = Imagem(
        id=str(uuid.uuid4()),
        name= imagem.filename,
        data=imagem.read(),
        user_id=user.id
    )
    
    if teste=='True':
        user.confirmed = True
    #Salvando os objetos no banco de dados
    db.session.add(imagemObject)
    db.session.add(user)
    db.session.commit()

    if teste!='True':
        #Função para enviar o codigo de verificação par ao usuario
        send_email(email, 'Confirmação de email', user.generateCode(),name )

    return (
        jsonify(
            {
                "user": user.profileDict(),
                "imagem": imagemObject.profileDict()
            }
        ),
        201,
    )

#Rota para confirmar o codigo enviado pelo email
@user.route('/confirmedCode/<string:id>', methods=['POST'])
def confirmedCodeUser(id):

    request_data = request.get_json()
    
    # Checar se todos os dados foram fornecidos
    if not (
        (
            request_data.get("code")
        )
    ):
        return jsonify({"message": "É preciso o codigo de verificação"}), 400
    
    #Verificando se os dados estão na formatação correta
    if type(request_data.get("code"))!=str:
        return ("É preciso que codigo seja fornecido em string!"),400
    
    #Consulta com o id fornecido
    user = User.query.get(id)

    #Tratando possiveis erros
    if not user:
        return jsonify({"message": "Usuario não encontrado!"}), 400
    
    if user.confirmed == True:
        return jsonify({"message": "Usuario já tem sua conta confirmada!"}), 400
    
    #Confirmando o codigo
    confirmed = user.confirmedCode(request_data.get("code"))

    if confirmed == True:
         return (
        jsonify(
            {
                "user": user.profileDict()
            }
        ),
        200,
    )
    else:
        return jsonify({"message": "Não foi possivel verificar a conta, verifique se o codigo estar correto e tente novamente!"}), 400

#Rota para reenviar o codigo de verificação
@user.route('/resendCode/<string:id>', methods=['POST'])
def resendCode(id):

    #Consulta com o id fornecido
    user = User.query.get(id)

    #Tratando possiveis erros
    if not user:
        return jsonify({"message": "Usuario não encontrado!"}), 400
    
    if user.confirmed == True:
        return jsonify({"message": "Usuario já tem sua conta confirmada!"}), 400
    
    #Enviando novamente o email para o cliente com o codigo de verificação
    send_email(user.email, 'Confirmação de email', user.generateCode(),user.name )

    return jsonify({"message": "Email com o código de verificação foi novamente enviado!"}), 400

#Rota para realizar update no perfil do usuario
@user.route('/updateProfile', methods=['PUT'])
@is_valid_token
def updateProfile():
    request_data = request.get_json()
    email = False
    #Consulta com o id fornecido pelo token
    user: User = g.get("current_user")

    #Verificando quais campos o usuario quer realizar o update
    #Update do nome
    if (request_data.get('name')):
        user.name = request_data.get('name')
    
    #Update do email, antes de realizar o email é verificado se já existe algum email igual 
    # e se não tiver o usuario tem que confirmar a conta novamente
    if (request_data.get('email')):
        if db.session.query(
            exists().where((User.email == request_data.get("email")))
        ).scalar():
            return jsonify({"message": "Email já cadastrado!"}), 400
        
        email= True
        user.email = request_data.get('email')
        if teste!='True':
            user.confirmed = False

    #Update cpf, primeiro é verificado se existe alfum cpf igual se não existir
    # é feito uma validação para que o usaurio forneça um cpf valido
    if(request_data.get('cpf')):
        if db.session.query(
            exists().where((User.cpf == request_data.get("cpf")))
        ).scalar():
            return jsonify({"message": "Cpf já cadastrado!"}), 400
        
        if teste!='True':
            if validar_cpf(request_data.get('cpf')):
                user.cpf = request_data.get('cpf')

            else:
                return jsonify({"message": "Cpf invalido!"}), 400
        else:
            user.cpf = request_data.get('cpf')
    #Update de telefone, é verificado se existe outro telefone igual
    if(request_data.get('phone')):
        if db.session.query(
            exists().where((User.phone == request_data.get("phone")))
        ).scalar():
            return jsonify({"message": "Telefone já cadastrado!"}), 400
        
        user.phone = request_data.get('phone')
    
    #Update da data de nascimento
    if(request_data.get('birth_date')):
        formato = "%d/%m/%Y"
        user.birth_date = datetime.strptime(request_data.get('birth_date'), formato)

    # Se o email for trocado é enviado novamente o codigo de confirmação e o usuario é deslogado da prataforma
    if email == True and  teste!='True':
        send_email(request_data.get('email'), 'Confirmação do novo email', user.generateCode(),user.name )
        user.revoke_token()
        db.session.commit()
        return (
            jsonify(
                {
                    "user": user.profileDict(),
                    "email":'Email enviado para confirmação do novo código, confirme o email e faça o login novamente!'
                }
            ),
            200,
        )
    db.session.commit()
    return (
        jsonify(
            {
                "user": user.profileDict()
            }
        ),
        200,
    )

        
