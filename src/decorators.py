from functools import wraps
from flask import g, request, current_app
from dbModel import User

#Decorrator para validar o email e a senha do usuario
def valid_credentials(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_data = request.get_json()
        if request_data.get("email") and request_data.get("password"):
            user = User.query.filter_by(email=request_data.get("email")).first()
            if not user or not user.verify_password(request_data.get("password")):
                return ("E-mail ou senha inválidos."),405
            g.current_user = user

            return f(*args, **kwargs)
        return ("Faltam credenciais."),400

    return decorated_function

#Decorrator para validar o token do usuario
def is_valid_token(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "OPTIONS":
            return
        try:
            token = request.headers.get("Authorization").split()[1]
        except Exception:
            return ("Token inválido"),400
        
        g.current_user = User.verify_token(token)
        if g.get("current_user") is None:
            return ("Token inválido - Usuário"),401
       
        return f(*args, **kwargs)

    return decorated_function