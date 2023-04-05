import uuid
import random
from flask import Blueprint, jsonify
from models.dbModel import db, Filmes, Role, Livros, Series, User
dataBase = Blueprint('dataBase', __name__)

@dataBase.route('/inicializarBanco',methods=['POST'])
def inicializar_banco():
    """Rota para inicializar o banco de dados

    ---
    tags:
        - DATA BASE
    
                
    responses:
      200:
        description: Login realizado com sucesso
        examples:
          application/json:
            {
               "message": "Banco de dados inicializado e pre populado com sucesso!"
            }
         
    
    """
    db.create_all()

    # Criando os Roles
    Role.insert_roles()
    db.session.commit()

    # Admin 
    admin: User = User(
        id = str(uuid.uuid4()),
        email="admin@admin.com",
        name="ADMIN",
        password="123456",
        confirmed=True
    )
    db.session.add(admin)
    db.session.commit()

    #Pre populando o banco assim que inicializar
    for i in range(100):
        # Criando Filmes
        comeco = ['Aventura', 'Super', 'Os', 'Mal', 'Jogos', 'Fim', 'Amor']
        meio = ['bruxos', 'ninjas', 'lutador', 'ditador', 'felicidade', 'jogador', 'game']
        fim = ['I.', 'III', 'III', 'ultimato', 'final', 'parte I', 'parte II']
        nome =  f'{random.choice(comeco)} {random.choice(meio)} {random.choice(fim)}'
        filme = Filmes(
            id=str(uuid.uuid4()),
            name = nome,
            descricao = 'O filme '+ nome+' fala de uma historia baseada em fatos reais',
            avaliacao = str(random.randint(0, 5)),
            anoLancamento = random.randint(1930,2023)
        )
        db.session.add(filme)
        
        # Criando Livros
        comeco = ['A', 'As', 'Os', 'O', 'Super', 'Inimigos', 'Amor']
        meio = ['bruxos', 'ninjas', 'lutador', 'ditador', 'felicidade', 'jogador', 'game']
        fim = ['poderosos.', 'animais', 'natureza', 'tecnologia', '3', '2', 'final']
        autorNome = ['Ana', 'Bianca', 'Carlos', 'Diego', 'Eduarda', 'Fernanda', 'Gabriel', 'Helena', 'Isabella', 'João']
        autorSobrenome = ['Silva', 'Souza', 'Ferreira', 'Oliveira', 'Costa', 'Pereira', 'Rodrigues', 'Almeida', 'Gomes', 'Lima']
        livro = Livros(
            id=str(uuid.uuid4()),
            name = f'{random.choice(comeco)} {random.choice(meio)} {random.choice(fim)}',
            autor = f'{random.choice(autorNome)} {random.choice(autorSobrenome)} ',
            avaliacao = str(random.randint(0, 5)),
            anoLancamento = random.randint(1930,2023)
        )
        db.session.add(livro)

        # Criando Series
        comeco = ['Academia', 'Lago', 'Mundo', 'Panico', 'Jogos', 'Computador', 'Exteminador']
        meio = ['maquinas', 'atirador', 'lutador', 'poeta', 'animal', 'leão', 'game']
        fim = ['I.', 'III', 'III', 'ultimato', 'final', 'parte I', 'parte II']
        nome =  f'{random.choice(comeco)} {random.choice(meio)} {random.choice(fim)}'
        serie = Series(
            id=str(uuid.uuid4()),
            name = nome,
            descricao = 'A serie '+ nome+' fala de uma historia baseada em fatos reais',
            avaliacao = str(random.randint(0, 5)),
            anoLancamento = random.randint(1930,2023)
        )
        db.session.add(serie)
        
    db.session.commit()

    return jsonify({"message": "Banco de dados inicializado e pre populado com sucesso!"}), 201