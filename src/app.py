from flask import Flask
from dbModel import db,SQLALCHEMY_DATABASE_URI


#Configurando o aplicativo flask 
app = Flask(__name__)

#Configurando o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
#Registrando os blueprints
from user.user import user
app.register_blueprint(user, url_prefix='/user')

from initDb.initDb import dataBase
app.register_blueprint(dataBase, url_prefix='/dataBase')

from autentication.autentication import autentication
app.register_blueprint(autentication, url_prefix='/autentication')

from loginArea.public.public import public
app.register_blueprint(public, url_prefix='/public')

from loginArea.privade.vip import vip
app.register_blueprint(vip, url_prefix='/vip')

from admin.admin import admin
app.register_blueprint(admin, url_prefix='/admin')


# inicializando a aplicação
if __name__ == '__main__':
    app.run(debug=True)
