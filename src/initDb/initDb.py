import uuid
import random
from flask import Blueprint, jsonify
from dbModel import db, Filmes
dataBase = Blueprint('dataBase', __name__)

@dataBase.route('/inicializarBanco',methods=['POST'])
def inicializar_banco():
    db.create_all()

    #Pre populando o banco assim que inicializar
    for i in range(100):
        comeco = ['Aventura', 'Super', 'Os', 'Mal', 'Jogos', 'Fim', 'Amor']
        fim = ['I.', 'III', 'III', 'ultimato', 'final', 'parte I', 'parte II']
        meio = ['bruxos', 'ninjas', 'lutador', 'ditador', 'felicidade', 'jogador', 'game']
        nome =  f'{random.choice(comeco)} {random.choice(meio)} {random.choice(fim)}'
        print (nome)
        filme = Filmes(
            id=str(uuid.uuid4()),
            name = nome,
            descricao = 'O filme '+ nome+' fala de uma historia baseada em fatos reais',
            avaliacao = str(random.randint(0, 5)),
            anoLancamento = random.randint(1930,2023)
        )
        db.session.add(filme)
    
    db.session.commit()

    return jsonify({"message": "Banco de dados inicializado e pre populado com sucesso!"}), 201