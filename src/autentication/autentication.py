from flask import jsonify, g, Blueprint, send_from_directory, request
from decorators import valid_credentials, is_valid_token
from dbModel import db, User

autentication = Blueprint('autentication', __name__)

#Rota para login
@autentication.route('/login', methods=["POST"])
@valid_credentials
def login():
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
    user : User = g.current_user
    user.revoke_token()
    db.session.commit()
    return jsonify({"message": "Logout successfully"}), 200


#Rota para visualização do termo de uso
@autentication.route('/termoUso', methods=["GET"])
def termoUso():
   directory = 'pdf'
   pdf_filename = 'termo.pdf'
   return send_from_directory(directory, pdf_filename, as_attachment=True)


#Rota para trocar a senha do usuario
@autentication.route('/chargePassword', methods=["PUT"])
@valid_credentials
@is_valid_token
def resetPassword():
    request_data = request.get_json()
    
    user: User = g.get("current_user")
    
    user.change_password(request_data.get("newPassword"))
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Senha alterada com sucesso!"}), 200
