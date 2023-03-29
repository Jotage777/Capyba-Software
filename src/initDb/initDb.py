from flask import Blueprint
from dbModel import db
dataBase = Blueprint('dataBase', __name__)

@dataBase.route('/inicializarBanco',methods=['POST'])
def inicializar_banco():
    db.create_all()
    return 'Banco de dados inicializado!'