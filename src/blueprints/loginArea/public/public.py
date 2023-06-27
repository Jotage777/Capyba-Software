from flask import jsonify, g, Blueprint, request
from decorators.decorators import is_valid_token
from models.dbModel import Filmes, to_dict

from sqlalchemy import or_
public = Blueprint('pubic', __name__)


#Rota para pessoas logadas na área publica
@public.route('/filmes',methods=["GET"])
@is_valid_token
def getListFilmes():
    """Rota para realizar consultas na area publica, na parte de Filme

    ---
    tags:
        - AREA LOGADA - PUBLIC
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
        description: Filme adicionado
        examples:
          application/json:
            {
               "A.info":{
                    "Page": page ,
                    "Page size": pageSize,
                    "Itens totais": todos os itens
                    },
                    "Filme": [
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
        ordering = Filmes.avaliacao
    else:
        if ordering == 'name':
            ordering = Filmes.name
        
        elif ordering == 'descricao':
            ordering = Filmes.descricao
        
        elif ordering == 'avaliacao':
            ordering = Filmes.avaliacao

        elif ordering == 'anoLancamento':
            ordering = Filmes.anoLancamento
        
        else:
            return jsonify({"message": "Ordenação não permitida!Tente novamente com name, descricao,avaliacao ou anoLancamento"}), 400
    
    

    if (not search) and (not assessment) and (not id):
        filmes = Filmes.query.order_by(ordering.desc()).paginate(per_page=pageSize, page = page, error_out=True)
    
    elif( search and id) or (search and assessment) or (assessment and id):
         return jsonify({"message": "Os parametros id, search e assessment só podem ser consultados de forma separada!"}), 400
    
    elif search:
        filmes = Filmes.query.filter(or_(Filmes.name.like(f'%{search}%'), Filmes.descricao.like(f'%{search}%'))).order_by(ordering.desc()).paginate(per_page=pageSize, page = page, error_out=True)

    elif assessment:
        filmesAssessment = Filmes.query.filter_by(avaliacao=assessment).all()
        filmes_dict = [filmes.profileDictPublic() for filmes in filmesAssessment]
        return (
        jsonify(
            {   "A.info":{
                "Page": page ,
                "Page_size": len(filmesAssessment),
                "Itens_totais":Filmes.query.count()
                },
                "Filmes": filmes_dict

            }
        ),
        200,
    )

    elif id:
        filme = Filmes.query.get(id)
        if filme is None:
            return (
            jsonify(
                {   "A.info":{
                    "Page": page ,
                    "Page_size": 0,
                    "Itens_totais":Filmes.query.count()
                    },
                    "Filmes": []

                }
            ),
            200,)
        
        return (
        jsonify(
            {   "A.info":{
                "Page": page ,
                "Page_size": 1,
                "Itens_totais":Filmes.query.count()
                },
                "Filmes": filme.profileDictPublic()

            }
        ),
        200,
    )


    if filmes is not None:
        filmes_dict = [to_dict(filme) for filme in filmes.items]
   
    return (
        jsonify(
            {   "A.info":{
                "Page": page ,
                "Page_size": len(filmes_dict),
                "Itens_totais":Filmes.query.count()
                },
                "Filmes": filmes_dict

            }
        ),
        200,
    )

    