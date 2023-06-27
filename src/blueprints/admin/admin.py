from flask import jsonify, g, Blueprint, request
from decorators.decorators import is_valid_token, hasPermissionAdmin
from models.dbModel import Filmes, Livros, Series,User,Permission,Role,Imagem, db
import uuid


admin = Blueprint('admin', __name__)

#Rota par adicionar um filme
@admin.route('/addFilme',methods=["POST"])
@is_valid_token
@hasPermissionAdmin
def addFilme():
    """Rota para adicionar um novo filme através do ADMIN

    ---
    tags:
        - ADMIN
    parameters:
      - in: body
        description: Request body
        schema:
          type: object
          properties:
            nome:
              type: string
              require: true
              example: "João Gabriel"
            descricao:
              type: string
              require: true
              example: "DEscrição do filme"
            avaliacao:
              type: int
              require: true
              example: 5
            anoLancamento:
              type: int
              require: true
              example: 2023
      - name: Authorization
        in: header
        description: Token de acesso JWT
        required: true
        type: string
    
    responses:
      201:
        description: Filme adicionado
        examples:
          application/json:
            {
               Filme:{
                  "id":"string",
                  "name":"string",
                  "avaliação": "int",
                  "ano de lançamento": "int"
               }
            }
      400:
        description: Faltando alguma informação
        examples:
          application/json:
            {
               "Mensagem":"É preciso o nome, decrição, avaliação e ano de lançamento"
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
      403:
        description: O Usuario não é admin
        examples:
          application/json:
            {
               "message":"Usuário não tem permissão para acessar essa rota."
            }
    
    """
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
    """Rota para adicionar um novo filme através do ADMIN

    ---
    tags:
        - ADMIN
    parameters:
      - in: body
        description: Request body
        schema:
          type: object
          properties:
            nome:
              type: string
              require: true
              example: "Livro"
            autor:
              type: string
              require: true
              example: "Gabriel Oliveira"
            avaliacao:
              type: int
              require: true
              example: 5
            anoLancamento:
              type: int
              require: true
              example: 2023
      - name: Authorization
        in: header
        description: Token de acesso JWT
        required: true
        type: string
    
    responses:
      201:
        description: Serie adicionado
        examples:
          application/json:
            {
               Serie:{
                  "id":"string",
                  "autor":"string",
                  "avaliação": "int",
                  "ano de lançamento": "int"
               }
            }
      400:
        description: Faltando alguma informação
        examples:
          application/json:
            {
               "Mensagem":"É preciso o nome, autor, avaliação e ano de lançamento"
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
      403:
        description: O Usuario não é admin
        examples:
          application/json:
            {
               "message":"Usuário não tem permissão para acessar essa rota."
            }
    
    """
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
    """Rota para adicionar um novo livro através do ADMIN

    ---
    tags:
        - ADMIN
    parameters:
      - in: body
        description: Request body
        schema:
          type: object
          properties:
            nome:
              type: string
              require: true
              example: "João Gabriel"
            descricao:
              type: string
              require: true
              example: "Descrição do livro"
            avaliacao:
              type: int
              require: true
              example: 5
            anoLancamento:
              type: int
              require: true
              example: 2023
      - name: Authorization
        in: header
        description: Token de acesso JWT
        required: true
        type: string
    responses:
      201:
        description: Filme adicionado
        examples:
          application/json:
            {
               "Livro":{
                  "id":"string",
                  "name":"string",
                  "avaliação": "int",
                  "ano de lançamento": "int"
               }
            }
      400:
        description: Faltando alguma informação
        examples:
          application/json:
            {
               "Mensagem":"É preciso o nome, decrição, avaliação e ano de lançamento"
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
      403:
        description: O Usuario não é admin
        examples:
          application/json:
            {
               "message":"Usuário não tem permissão para acessar essa rota."
            }
    
    """
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
    """Rota para conceder permissão para o usuario acessar a area vip

    ---
    tags: 
      - ADMIN
    parameters:
      - in: body
        description: Request body
        schema:
          type: object
          properties:
            role:
              type: string
              require: true
              example: "VIP OU PUBLIC"
      - name: Authorization
        in: header
        description: Token de acesso JWT
        required: true
        type: string
    
    responses:
      200:
        description: Permissão alterada
        examples:
          application/json:
            {
               "message": "Permissão de usuário alterada com sucesso."
            }
      400:
        description: Role vazio ou não enviado
        examples:
          application/json:
            {
               "message": "Role não disponivel."
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
      400(4):
        description: Usuario já tem acesso vip
        examples:
          application/json:
            {
               "message": "Usuário já é um membro vip."
            }
      403:
        description: O Usuario não é admin
        examples:
          application/json:
            {
               "message":"Usuário não tem permissão para acessar essa rota."
            }
    """
    request_data = request.get_json()
    #Consulta com o id fornecido
    user = User.query.get(id)

    if(user.role.has_permission(Permission.VIP)):
        return jsonify({"message": "Usuário já é um membro vip."}), 400
    
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

    
@admin.route('/user/<string:id>', methods=["GET"])
@is_valid_token
def getUser(id):
    user = User.query.get(id)
    img = Imagem.query.filter_by(user_id=id).first()

    if user:
        return (
            jsonify(
                {
                    "User": user.profileDict(),
                    "Img": img.profileDict() if img else None
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "Usuário não encontrado."}), 404
  

@admin.route('/user',methods=["GET"])
@is_valid_token
def getAllUsers():
  page = request.args.get("page", type=int)
  pageSize = request.args.get("pageSize", type=int)

  if not page:
        page = 1
  if not pageSize:
      pageSize = 20
  
  ordering = User.name

  users_pagination = User.query.order_by(ordering.desc()).paginate(per_page=pageSize, page=page, error_out=True)
  users = users_pagination.items


  if users:
      users_dict = [user.profileDict() for user in users]
      return (jsonify({
          "A.info": {
              "Page": page,
              "Page_size": len(users),
              "Itens_totais": User.query.count()
          },
          "Users": users_dict,
          
      }), 200)
  else:
      return jsonify({"message": "Usuário não encontrado."}), 404
