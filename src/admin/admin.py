from flask import jsonify, g, Blueprint, request
from decorators import is_valid_token, hasPermissionAdmin
from dbModel import Filmes, Livros, Series,User,Permission,Role, db
import uuid


admin = Blueprint('admin', __name__)

#Rota par adicionar um filme
@admin.route('/addFilme',methods=["POST"])
@is_valid_token
@hasPermissionAdmin
def addFilme():
    request_data = request.get_json()

     # Checar se todos os dados foram fornecidos
    if not (
        (
            request_data.get("nome")
            and request_data.get('descricao')
            and request_data.get('avaliacao')
            and request_data.get("anoLancamento")
        )
    ):
        return jsonify({"message": "É preciso o nome, decrição, avaliação e ano de lançamento"}), 400
    
    filme = Filmes(
        id = str(uuid.uuid4()),
        name = request_data.get("nome"),
        descricao = request_data.get('descricao'),
        avaliacao = request_data.get('avaliacao'),
        anoLancamento = request_data.get("anoLancamento")
    )
    db.session.add(filme)
    db.session.commit()

    return (
        jsonify(
            {
                "Filme": filme.profileDictPublic(),
            }
        ),
        201,
    )

#Rota par adicionar um Serie
@admin.route('/addSerie',methods=["POST"])
@is_valid_token
@hasPermissionAdmin
def addSerie():
    request_data = request.get_json()

     # Checar se todos os dados foram fornecidos
    if not (
        (
            request_data.get("nome")
            and request_data.get('descricao')
            and request_data.get('avaliacao')
            and request_data.get("anoLancamento")
        )
    ):
        return jsonify({"message": "É preciso o nome, decrição, avaliação e ano de lançamento"}), 400
    
    serie = Series(
        id = str(uuid.uuid4()),
        name = request_data.get("nome"),
        descricao = request_data.get('descricao'),
        avaliacao = request_data.get('avaliacao'),
        anoLancamento = request_data.get("anoLancamento")
    )
    db.session.add(serie)
    db.session.commit()

    return (
        jsonify(
            {
                "Serie": serie.profileDictPublic(),
            }
        ),
        201,
    )


#Rota par adicionar um livro
@admin.route('/addLivro',methods=["POST"])
@is_valid_token
@hasPermissionAdmin
def addLivro():
    request_data = request.get_json()

     # Checar se todos os dados foram fornecidos
    if not (
        (
            request_data.get("nome")
            and request_data.get('autor')
            and request_data.get('avaliacao')
            and request_data.get("anoLancamento")
        )
    ):
        return jsonify({"message": "É preciso o nome, decrição, avaliação e ano de lançamento"}), 400
    
    livro = Livros(
        id = str(uuid.uuid4()),
        name = request_data.get("nome"),
        autor = request_data.get('autor'),
        avaliacao = request_data.get('avaliacao'),
        anoLancamento = request_data.get("anoLancamento")
    )
    db.session.add(livro)
    db.session.commit()

    return (
        jsonify(
            {
                "Livro": livro.profileDictPublic(),
            }
        ),
        201,
    )

#Rota para alterar permissão
@admin.route('/editRole/<string:id>',methods=["PUT"])
@is_valid_token
@hasPermissionAdmin
def editRole(id):
    request_data = request.get_json()
    #Consulta com o id fornecido
    user = User.query.get(id)

    if(user.role.has_permission(Permission.VIP)):
        return jsonify({"message": "Usuário já é um menbro vip."}), 403
    
    if(request_data.get('role')=='VIP'):
        user.role_id = Role.query.filter_by(name="VIP").first().id
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Permissão de usuário alterada com sucesso."}), 200
    
    elif(request_data.get('role')=='PUBLIC'):
        user.role_id = Role.query.filter_by(name="PUBLIC").first().id
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Permissão de usuário alterada com sucesso."}), 200
    
    else:
        return jsonify({"message": "Role não disponivel."}), 400
    

