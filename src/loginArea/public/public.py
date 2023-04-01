from flask import jsonify, g, Blueprint, request
from decorators import is_valid_token
from dbModel import Filmes, to_dict

from sqlalchemy import or_
public = Blueprint('pubic', __name__)


#Rota para pessoas logadas na área publica
@public.route('/filmes',methods=["GET"])
@is_valid_token
def getListFilmes():
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
                "Page size": len(filmesAssessment),
                "Itens totais":Filmes.query.count()
                },
                "Filmes": filmes_dict

            }
        ),
        200,
    )

    elif id:
        filme = Filmes.query.get(id)
        return (
        jsonify(
            {   "A.info":{
                "Page": page ,
                "Page size": 1,
                "Itens totais":Filmes.query.count()
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
                "Page size": len(filmes_dict),
                "Itens totais":Filmes.query.count()
                },
                "Filmes": filmes_dict

            }
        ),
        200,
    )

    