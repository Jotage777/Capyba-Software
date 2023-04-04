from flask import Flask, jsonify
from models.dbModel import db, SQLALCHEMY_DATABASE_URI
from flasgger import Swagger


#Configurando o aplicativo flask 
app = Flask(__name__)

#Configurando o swagger
swagger = Swagger(app)

#Configurando o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)

#Registrando os blueprints
from blueprints.user.user import user
app.register_blueprint(user, url_prefix='/user')

from models.initDb.initDb import dataBase
app.register_blueprint(dataBase, url_prefix='/dataBase')

from blueprints.autentication.autentication import autentication
app.register_blueprint(autentication, url_prefix='/autentication')

from blueprints.loginArea.public.public import public
app.register_blueprint(public, url_prefix='/public')

from blueprints.loginArea.privade.vip import vip
app.register_blueprint(vip, url_prefix='/vip')

from blueprints.admin.admin import admin
app.register_blueprint(admin, url_prefix='/admin')

# inicializando a aplicação
if __name__ == '__main__':
    app.run(debug=True)
