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

# inicializando a aplicação
if __name__ == '__main__':
    app.run(debug=True)