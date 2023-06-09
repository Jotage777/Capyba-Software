from flask import jsonify, g, Blueprint, request
from decorators.decorators  import is_valid_token, hasPermissionVip
from models.dbModel import Livros, Series, to_dict
from sqlalchemy import or_

vip = Blueprint('vip', __name__)

#Rota para livros na area vip
@vip.route('/livros',methods=["GET"])
@is_valid_token
@hasPermissionVip
def getListLivros():
    """Rota para realizar consultas na area privada, na parte de livros

    ---
    tags:
        - AREA LOGADA - VIP
    parameters:
      - name: page
        in: query
        description: Número da página que deve ser retornada
        type: integer
        required: false

      - name: pageSize
        in: query
        description: Número de itens retornados da pagina
        type: integer
        required: false

      - name: search
        in: query
        description: Para pesquisar alguma palavra no nome do livro
        type: string
        required: false

      - name: ordering
        in: query
        description: Qual o filtro que a ordenação que deve seguir
        type: string
        required: false

      - name: assessment
        in: query
        description: Filtrar pelo numero de avaliação
        type: integer
        required: false
    
      - name: id
        in: query
        description: Consultar algum livro que tenha esse id
        type: string
        required: false

      - name: Authorization
        in: header
        description: Token de acesso JWT
        required: true
        type: string
    
    responses:
      200:
        description: Livro adicionado
        examples:
          application/json:
            {
               "A.info":{
                    "Page": page ,
                    "Page size": pageSize,
                    "Itens totais": todos os itens
                    },
                    "Livro": [
                        {
                        "id": id,
                        "name": name,
                        "Autor": autor,
                        "avaliação": avaliacao,
                        "ano de lançamento": anoLancamento
                        }
                    ]

            }
      400:
        description: Ordenação não permitida
        examples:
          application/json:
            {
               message": "Ordenação não permitida!Tente novamente com name, autor, avaliacao ou anoLancamento"
            }
      400(2):
        description: Query não permitida
        examples:
          application/json:
            {
               "message": "Os parametros id, search e assessment só podem ser consultados de forma separada!"
            }
      400(3):
        description: Token expirou
        examples:
          application/json:
            {
               "message":" Token inválido."
            }
      400(4):
        description: Token errado
        examples:
          application/json:
            {
               "message":"Token inválido - Usuário."
            }
      403:
        description: O Usuario não é vip
        examples:
          application/json:
            {
               "message":"Usuário não tem permissão para acessar essa rota."
            }
    
    """
    page = request.args.get("page", type=int)
    pageSize = request.args.get("pageSize", type=int)
    search = request.args.get("search", type=str)
    ordering = request.args.get("ordering", type=str)
    assessment = request.args.get("assessment", type=int)
    id = request.args.get("id", type=str)

    if not page:
        page = 1
    if not pageSize:
        pageSize = 20
    if not ordering:
        ordering = Livros.avaliacao
    else:
        if ordering == 'name':
            ordering = Livros.name
        
        elif ordering == 'autor':
            ordering = Livros.autor
        
        elif ordering == 'avaliacao':
            ordering = Livros.avaliacao

        elif ordering == 'anoLancamento':
            ordering = Livros.anoLancamento
        
        else:
            return jsonify({"message": "Ordenação não permitida!Tente novamente com name, autor, avaliacao ou anoLancamento"}), 400
    
    if (not search) and (not assessment) and (not id):
        livros = Livros.query.order_by(ordering.desc()).paginate(per_page=pageSize, page = page, error_out=True)
    
    elif( search and id) or (search and assessment) or (assessment and id):
         return jsonify({"message": "Os parametros id, search e assessment só podem ser consultados de forma separada!"}), 400
    
    elif search:
        livros = Livros.query.filter(or_(Livros.name.like(f'%{search}%'), Livros.autor.like(f'%{search}%'))).order_by(ordering.desc()).paginate(per_page=pageSize, page = page, error_out=True)

    elif assessment:
        livroAssessment = Livros.query.filter_by(avaliacao=assessment).all()
        livros_dict = [livros.profileDictPublic() for livros in livroAssessment]
        return (
        jsonify(
            {   "A.info":{
                "Page": page ,
                "Page size": len(livroAssessment),
                "Itens totais":Livros.query.count()
                },
                "Livros": livros_dict

            }
        ),
        200,
    )

    elif id:
        livro = Livros.query.get(id)
        if livro is None:
            return (
            jsonify(
                {   "A.info":{
                    "Page": page ,
                    "Page size": 0,
                    "Itens totais":Livros.query.count()
                    },
                    "Livro": []

                }
            ),
            200,)
        
        return (
        jsonify(
            {   "A.info":{
                "Page": page ,
                "Page size": 1,
                "Itens totais":Livros.query.count()
                },
                "Livro": livro.profileDictPublic()

            }
        ),
        200,
    )

    if livros is not None:
        livros_dict = [to_dict(livro) for livro in livros.items]

    return (
        jsonify(
            {   "A.info":{
                "Page": page ,
                "Page size": len(livros_dict),
                "Itens totais":Livros.query.count()
                },
                "Livros": livros_dict

            }
        ),
        200,
    )

#Rota de series para area vip
@vip.route('/series',methods=["GET"])
@is_valid_token
@hasPermissionVip
def getListSeries():
    """Rota para realizar consultas na area privada, na parte de series

    ---
    tags:
        - AREA LOGADA - VIP
    parameters:
      - name: page
        in: query
        description: Número da página que deve ser retornada
        type: integer
        required: false

      - name: pageSize
        in: query
        description: Número de itens retornados da pagina
        type: integer
        required: false

      - name: search
        in: query
        description: Para pesquisar alguma palavra no nome do livro
        type: string
        required: false

      - name: ordering
        in: query
        description: Qual o filtro que a ordenação que deve seguir
        type: string
        required: false

      - name: assessment
        in: query
        description: Filtrar pelo numero de avaliação
        type: integer
        required: false
    
      - name: id
        in: query
        description: Consultar algum livro que tenha esse id
        type: string
        required: false

      - name: Authorization
        in: header
        description: Token de acesso JWT
        required: true
        type: string
    
    responses:
      200:
        description: Serie adicionado
        examples:
          application/json:
            {
               "A.info":{
                    "Page": page ,
                    "Page size": pageSize,
                    "Itens totais": todos os itens
                    },
                    "Serie": [
                        {
                        "id": id,
                        "name": name,
                        "descrição": autor,
                        "avaliação": avaliacao,
                        "ano de lançamento": anoLancamento
                        }
                    ]

            }
      400:
        description: Ordenação não permitida
        examples:
          application/json:
            {
               message": "Ordenação não permitida!Tente novamente com name, descricao, avaliacao ou anoLancamento"
            }
      400(2):
        description: Query não permitida
        examples:
          application/json:
            {
               "message": "Os parametros id, search e assessment só podem ser consultados de forma separada!"
            }
      400(3):
        description: Token expirou
        examples:
          application/json:
            {
               "message":" Token inválido."
            }
      400(4):
        description: Token errado
        examples:
          application/json:
            {
               "message":"Token inválido - Usuário."
            }
      403:
        description: O Usuario não é vip
        examples:
          application/json:
            {
               "message":"Usuário não tem permissão para acessar essa rota."
            }
    
    """
    page = request.args.get("page", type=int)
    pageSize = request.args.get("pageSize", type=int)
    search = request.args.get("search", type=str)
    ordering = request.args.get("ordering", type=str)
    assessment = request.args.get("assessment", type=int)
    id = request.args.get("id", type=str)

    if not page:
        page = 1
    if not pageSize:
        pageSize = 20
    if not ordering:
        ordering = Series.avaliacao
    else:
        if ordering == 'name':
            ordering = Series.name
        
        elif ordering == 'descricao':
            ordering = Series.descricao
        
        elif ordering == 'avaliacao':
            ordering = Series.avaliacao

        elif ordering == 'anoLancamento':
            ordering = Series.anoLancamento
        
        else:
            return jsonify({"message": "Ordenação não permitida!Tente novamente com name, descricao, avaliacao ou anoLancamento"}), 400
    
    if (not search) and (not assessment) and (not id):
        series = Series.query.order_by(ordering.desc()).paginate(per_page=pageSize, page = page, error_out=True)
    
    elif( search and id) or (search and assessment) or (assessment and id):
         return jsonify({"message": "Os parametros id, search e assessment só podem ser consultados de forma separada!"}), 400
    
    elif search:
        series = Series.query.filter(or_(Series.name.like(f'%{search}%'), Series.descricao.like(f'%{search}%'))).order_by(ordering.desc()).paginate(per_page=pageSize, page = page, error_out=True)

    elif assessment:
        seriesAssessment = Livros.query.filter_by(avaliacao=assessment).all()
        series_dict = [series.profileDictPublic() for series in seriesAssessment]
        return (
        jsonify(
            {   "A.info":{
                "Page": page ,
                "Page size": len(seriesAssessment),
                "Itens totais":Series.query.count()
                },
                "Series": series_dict

            }
        ),
        200,
    )

    elif id:
        serie = Series.query.get(id)
        if serie is None:
            return (
            jsonify(
                {   "A.info":{
                    "Page": page ,
                    "Page size": 0,
                    "Itens totais":Series.query.count()
                    },
                    "Serie": []

                }
            ),
            200,)
        
        return (
        jsonify(
            {   "A.info":{
                "Page": page ,
                "Page size": 1,
                "Itens totais":Series.query.count()
                },
                "Serie": serie.profileDictPublic()

            }
        ),
        200,
    )

    if series is not None:
        series_dict = [to_dict(serie) for serie in series.items]

    return (
        jsonify(
            {   "A.info":{
                "Page": page ,
                "Page size": len(series_dict),
                "Itens totais":Series.query.count()
                },
                "Series": series_dict

            }
        ),
        200,
    )