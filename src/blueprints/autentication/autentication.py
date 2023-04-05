from flask import jsonify, g, Blueprint, send_from_directory, request
from decorators.decorators import valid_credentials, is_valid_token
from models.dbModel import db, User

autentication = Blueprint('autentication', __name__)

#Rota para login
@autentication.route('/login', methods=["POST"])
@valid_credentials
def login():
    """Rota para realizar login

    ---
    tags:
        - AUTH
    parameters:
      - in: body
        description: Request body
        schema:
          type: object
          properties:
            email:
              type: string
              require: true
              example: "email@email.com"
            password:
              type: string
              require: true
              example: "12345678"
            
    responses:
      200:
        description: Login realizado com sucesso
        examples:
          application/json:
            {
               user:{
                    "id": 'string',
                    "email": 'string',
                    "name": 'string',
                    "confirmed": 'bool',
                    "cpf": 'string',
                    "birth_date": 'string',
                    "phone": self.phone,
                    "role": self.role_id
                },
                token:'string',
                expires_in: 86400
            }
      400:
        description: Faltando alguma informação
        examples:
          application/json:
            {
               "message": "Faltam credenciais."
            }
      405:
        description: Email ou senha errado
        examples:
          application/json:
            {
               "message": "E-mail ou senha inválidos."
            }
    
    
    """
    user: User = g.get("current_user")
    if not user.confirmed:
        return ("Usuário ainda não confirmou e-mail."),400
    token = user.generate_token()
    db.session.commit()
    return jsonify(
        {"token": token, "user": user.profileDict(), "expires_in": 86400}
    )

#Rota para logout
@autentication.route('/logout', methods=["POST"])
@is_valid_token
def logout():
    """Rota para realizar logout

    ---
    tags:
        - AUTH
    parameters:
      - name: Authorization
        in: header
        description: Token de acesso JWT
        required: true
        type: string
                
    responses:
      200:
        description: Login realizado com sucesso
        examples:
          application/json:
            {
               "message": "Logout successfully"
            }
      400:
        description: Token expirado
        examples:
          application/json:
            {
               "message": "Token inválido."
            }
      400(2):
        description: Token errado
        examples:
          application/json:
            {
               message": "Token inválido - Usuário."
            }
    
    
    """
    user : User = g.current_user
    user.revoke_token()
    db.session.commit()
    return jsonify({"message": "Logout successfully"}), 200


#Rota para visualização do termo de uso
@autentication.route('/termoUso', methods=["GET"])
def termoUso():
   """Rota para mostrar o termo de uso em pdf

    ---
    tags:
        - AUTH
                    
    responses:
      200:
        description: Mostra o pdf
        
    
    
    """
   directory = 'pdf'
   pdf_filename = 'termo.pdf'
   return send_from_directory(directory, pdf_filename, as_attachment=True)


#Rota para trocar a senha do usuario
@autentication.route('/chargePassword', methods=["PUT"])
@valid_credentials
@is_valid_token
def resetPassword():
    """Rota para trocar a senha do usuario

    ---
    tags:
        - AUTH
    parameters:
      - in: body
        description: Request body
        schema:
          type: object
          properties:
            email:
              type: string
              require: true
              example: "email@email.com"
            password:
              type: string
              require: true
              example: "12345678"
            newPassword:
              type: string
              require: true
              example: "12345678"
            
    responses:
      200:
        description: Troca de senha realizada com sucesso
        examples:
          application/json:
            {
               "message": "Senha alterada com sucesso!"
            }
      400:
        description: Faltando alguma informação
        examples:
          application/json:
            {
               "message": "Faltam credenciais."
            }
      400(2):
        description: Token expirou
        examples:
          application/json:
            {
               "message":" Token inválido."
            }
      400(3):
        description: Token errado
        examples:
          application/json:
            {
               "message":"Token inválido - Usuário."
            }
      405:
        description: Email ou senha errado
        examples:
          application/json:
            {
               "message": "E-mail ou senha inválidos."
            }
    
    
    """
    request_data = request.get_json()
    
    user: User = g.get("current_user")
    
    user.change_password(request_data.get("newPassword"))
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Senha alterada com sucesso!"}), 200
