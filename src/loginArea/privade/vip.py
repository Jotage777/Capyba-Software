from flask import jsonify, g, Blueprint, request
from decorators import is_valid_token, hasPermissionVip
from dbModel import Livros, Series, to_dict
from sqlalchemy import or_

vip = Blueprint('vip', __name__)

#Rota para livros na area vip
@vip.route('/livros',methods=["GET"])
@is_valid_token
@hasPermissionVip
def getListLivros():
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