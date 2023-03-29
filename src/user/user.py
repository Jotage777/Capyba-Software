import uuid
from flask import Blueprint, request, jsonify
from dbModel import db, User, Imagem
from sqlalchemy import exists
from configEmail import send_email

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
    
    #Salvando os objetos no banco de dados
    db.session.add(imagemObject)
    db.session.add(user)
    db.session.commit()

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