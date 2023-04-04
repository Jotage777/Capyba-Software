import pytest
from models.dbModel import db, Role
import json
from app import app


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.drop_all()
        db.create_all()
        Role.insert_roles()
        db.session.commit()
    with app.test_client() as client:
        yield client

#Registrando um usuario e efetuando o login
def test_register_and_login(client):
    
    #Registrando um usuario
    file_name = "../tests/imagem.png"
    file_data = open(file_name, "rb")

    data_user = {
        "name": "Joao",
        "email": "gabrieloliveira_pb@hotmail.com",
        "password": "password123",
        "imagem": (file_data, "imagem.png")
    }
    user = client.post('/user/register', data = data_user)
    
    #Login
    login = client.post('/autentication/login', 
    data =json.dumps({
        "email":'gabrieloliveira_pb@hotmail.com',
        "password": "password123"
    }),
    content_type="application/json")
   
    assert user.status_code == 201
    assert login.status_code == 200
    assert 'Joao' in user.text
    assert "gabrieloliveira_pb@hotmail.com" in user.text

#Teste de autenticação
def test_autentication(client):
    #Login
    login = client.post('/autentication/login', 
    data =json.dumps({
        "email":'gabrieloliveira_pb@hotmail.com',
        "password": "password123"
    }),
    content_type="application/json")

    if login.status_code == 200:
        token = login.get_json()["token"]

    #Logout
    logout = client.post('/autentication/logout',
    headers={"Authorization": "Bearer {}".format(token)}
    )

    assert login.status_code == 200
    assert logout.status_code == 200

#Teste de update do do usuario e mudando a senha
def test_update_user_and_charge_password(client):
    #Login
    login = client.post('/autentication/login', 
    data =json.dumps({
        "email":'gabrieloliveira_pb@hotmail.com',
        "password": "password123"
    }),
    content_type="application/json")

    if login.status_code == 200:
        token = login.get_json()["token"]
    
    #update sem token
    updateNotToken = client.put('/user/updateProfile',
    data = json.dumps({
        "name": "João Gabriel",
        "cpf":"06180262403",
        "phone":"83977889944",
        "birth_date": "24/05/1999",
        "email":"joao.ponciano@.email.com"
    }),
    content_type="application/json"
    )

    #Update com token
    updateToken = client.put('/user/updateProfile',
    data = json.dumps({
        "name": "João Gabriel",
        "cpf":"06180262403",
        "phone":"83977889944",
        "birth_date": "24/05/1999",
        "email":"joao.ponciano@email.com"
    }),
    headers={"Authorization": "Bearer {}".format(token)},
    content_type="application/json"
    )

    #Trocando a senha sem token
    chargePasswordNotToken = client.put('/autentication/chargePassword',
    data = json.dumps({
        "email":"joao.ponciano@email.com",
        "password": "password123",
        "newPassword": "123456"
    }),
    content_type="application/json")

    #Trocando a senha com umaq token invalido
    chargePasswordTokenInvalid = client.put('/autentication/chargePassword',
    data = json.dumps({
        "email":"joao.ponciano@email.com",
        "password": "password123",
        "newPassword": "123456"
    }),
    headers={"Authorization": "Bearer {}".format('1245669855566698585')},
    content_type="application/json")

    #Trocando a senha
    chargePasswordToken = client.put('/autentication/chargePassword',
    data = json.dumps({
        "email":"joao.ponciano@email.com",
        "password": "password123",
        "newPassword": "123456"
    }),
    headers={"Authorization": "Bearer {}".format(token)},
    content_type="application/json")

    #Tentando realizar login com a senha antiga
    loginOld=client.post('/autentication/login', 
    data =json.dumps({
        "email":'gabrieloliveira_pb@hotmail.com',
        "password": "password123"
    }),
    content_type="application/json")

    #REalizando login com a senha nova
    loginNew=client.post('/autentication/login', 
    data =json.dumps({
        "email":'joao.ponciano@email.com',
        "password": "123456"
    }),
    content_type="application/json")



    assert updateNotToken.status_code == 400
    assert updateToken.status_code == 200
    assert chargePasswordNotToken.status_code == 400
    assert chargePasswordTokenInvalid.status_code==401
    assert chargePasswordToken.status_code == 200
    assert loginOld.status_code == 405
    assert loginNew.status_code==200

#Testando a area do admin    
def test_admin_area(client):
    
    #Registrando um usuario admin
    file_name = "../tests/imagem.png"
    file_data = open(file_name, "rb")

    data_user = {
        "name": "ADMIN",
        "email": "admin@admin.com",
        "password": "123456",
        "imagem": (file_data, "imagem.png")
    }
    addAdmin = client.post('/user/register', data = data_user)


    #Logando com o admin
    loginAdmin = client.post('/autentication/login', 
        data =json.dumps({
            "email":'admin@admin.com',
            "password": "123456"
    }),
    content_type="application/json")

    if loginAdmin.status_code == 200:
        tokenAdmin = loginAdmin.get_json()["token"]

    #logando com o usuario normal
    loginUser = client.post('/autentication/login', 
        data =json.dumps({
            "email":'joao.ponciano@email.com',
            "password": "123456"
    }),
    content_type="application/json")

    
    if loginUser.status_code == 200:
        tokenUser = loginUser.get_json()["token"]

    #Tentando acessar uma rota de admin sem ser admin
    addLivroNotAdmin =client.post('/admin/addLivro',
    data=json.dumps({
        "nome": "Livro teste 1",
        "autor": "Gabriel Oliveira",
        "avaliacao":5,
        "anoLancamento": 1987
    }),
    headers={"Authorization": "Bearer {}".format(tokenUser)},
    content_type="application/json")

    #Adicinando um livro com admin
    addLivroAdmin = client.post('/admin/addLivro',
    data=json.dumps({
        "nome": "Livro teste 1",
        "autor": "Gabriel Oliveira",
        "avaliacao":5,
        "anoLancamento": 1987
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    #Adcionando uma serie sem ser admin
    addSerieNotAdmin =client.post('/admin/addSerie',
    data=json.dumps({
        "nome": "Serie teste 1",
        "descricao": "Descrição da serie",
        "avaliacao":2,
        "anoLancamento": 1999
    }),
    headers={"Authorization": "Bearer {}".format(tokenUser)},
    content_type="application/json")

    #adicionando com admin
    addSerieAdmin = client.post('/admin/addSerie',
    data=json.dumps({
        "nome": "Serie teste 1",
        "descricao": "Descrição da serie",
        "avaliacao":2,
        "anoLancamento": 1999
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    #Adicionando um filme sem ser admin
    addFilmeNotAdmin =client.post('/admin/addFilme',
    data=json.dumps({
        "nome": "Filme teste 1",
        "descricao": "Descrição do Filme",
        "avaliacao":2,
        "anoLancamento": 1999
    }),
    headers={"Authorization": "Bearer {}".format(tokenUser)},
    content_type="application/json")

    #Adicionando um filme com admin
    addFilmeAdmin = client.post('/admin/addFilme',
    data=json.dumps({
        "nome": "Filme teste 1",
        "descricao": "Descrição do Filme",
        "avaliacao":2,
        "anoLancamento": 1999
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    client.post('/admin/addFilme',
    data=json.dumps({
        "nome": "Filme teste 1",
        "descricao": "Descrição do Filme",
        "avaliacao":2,
        "anoLancamento": 1999
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    # Prepopulando o banco para o proximo teste

    client.post('/admin/addFilme',
    data=json.dumps({
        "nome": "Aventura",
        "descricao": "Descrição do Filme",
        "avaliacao":5,
        "anoLancamento": 1999
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    client.post('/admin/addFilme',
    data=json.dumps({
        "nome": "Filme Ação",
        "descricao": "Descrição do Filme",
        "avaliacao":3,
        "anoLancamento": 2001
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    client.post('/admin/addLivro',
    data=json.dumps({
        "nome": "Teste",
        "autor": "Gabriel Oliveira",
        "avaliacao":1,
        "anoLancamento": 2000
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    client.post('/admin/addLivro',
    data=json.dumps({
        "nome": "Gibi",
        "autor": "Oliveira",
        "avaliacao":5,
        "anoLancamento": 1977
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    client.post('/admin/addSerie',
    data=json.dumps({
        "nome": "Jogos",
        "descricao": "Descrição da serie",
        "avaliacao":2,
        "anoLancamento": 1956
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    client.post('/admin/addSerie',
    data=json.dumps({
        "nome": "Serie ação",
        "descricao": "Descrição da serie",
        "avaliacao":4,
        "anoLancamento": 1922
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")



    assert addAdmin.status_code==201
    assert addLivroNotAdmin.status_code == 403
    assert addLivroAdmin.status_code == 201
    assert addSerieNotAdmin.status_code == 403
    assert addSerieAdmin.status_code == 201
    assert addFilmeNotAdmin.status_code == 403
    assert addFilmeAdmin.status_code == 201

#Testando a area publica
def test_area_public(client):
    #Login com admin e usuario
    loginAdmin = client.post('/autentication/login', 
        data =json.dumps({
            "email":'admin@admin.com',
            "password": "123456"
    }),
    content_type="application/json")

    if loginAdmin.status_code == 200:
        tokenAdmin = loginAdmin.get_json()["token"]

    loginUser = client.post('/autentication/login', 
        data =json.dumps({
            "email":'joao.ponciano@email.com',
            "password": "123456"
    }),
    content_type="application/json")

    
    if loginUser.status_code == 200:
        tokenUser = loginUser.get_json()["token"]

    #Acessando sem token
    areaPublicNotToken = client.get('/public/filmes')
    
    #Consultando todos os filmes
    areaPublic = client.get('/public/filmes', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando com filtro de pesquisa
    areaPublicSearch = client.get('/public/filmes?search=1', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando com paginação
    areaPublicPage = client.get('/public/filmes?page=2&pageSize=1', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando o tamanho da paginação
    areaPublicPageSize = client.get('/public/filmes?pageSize=1', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por um filtro que não existe
    areaPublicOrdering400 = client.get('/public/filmes?ordering=1', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenado por ano
    areaPublicOrderingAno = client.get('/public/filmes?ordering=anoLancamento', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por nome
    areaPublicOrderingName = client.get('/public/filmes?ordering=name', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando com descrição
    areaPublicOrderingDescricao = client.get('/public/filmes?ordering=descricao', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por avaliação
    areaPublicOrderingAvaliacao = client.get('/public/filmes?ordering=avaliacao', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando por avaliação
    areaPublicAssessment = client.get('/public/filmes?assessment=5', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Adicionando um filme para consultar o seu id posteriormente
    addFilmeAdmin = client.post('/admin/addFilme',
    data=json.dumps({
        "nome": "Filme com o id",
        "descricao": "Gabriel Oliveira",
        "avaliacao":5,
        "anoLancamento": 1987
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    if addFilmeAdmin.status_code == 201:
        filmeid = addFilmeAdmin.get_json()['Filme']['id']
    
    areaPublicId = client.get('/public/filmes?id='+filmeid, headers={"Authorization": "Bearer {}".format(tokenUser)})


    assert areaPublicNotToken.status_code ==400
    assert areaPublic.status_code ==200
    assert areaPublic.get_json()['A.info']['Page'] == 1
    assert areaPublic.get_json()['A.info']['Page size'] == areaPublic.get_json()['A.info']['Itens totais']
    assert areaPublicSearch.status_code == 200
    assert areaPublicSearch.get_json()['A.info']['Page size'] < areaPublicSearch.get_json()['A.info']['Itens totais']
    assert areaPublicPage.status_code == 200
    assert areaPublicPage.get_json()['A.info']['Page'] == 2
    assert areaPublicPageSize.status_code == 200
    assert areaPublicPageSize.get_json()['A.info']['Page size'] == 1
    assert areaPublicOrdering400.status_code == 400
    assert areaPublicOrderingAno.status_code ==200
    assert areaPublicOrderingName.status_code ==200
    assert areaPublicOrderingDescricao.status_code ==200
    assert areaPublicOrderingAvaliacao.status_code ==200
    assert areaPublicAssessment.status_code == 200
    assert areaPublicAssessment.get_json()['A.info']['Page size'] < areaPublicAssessment.get_json()['A.info']['Itens totais']
    assert areaPublicId.status_code == 200
    assert areaPublicId.get_json()['Filmes']['id'] == filmeid

#Testando a area privada ou vip
def test_area_vip(client):
    #Login de admin e usuario
    loginAdmin = client.post('/autentication/login', 
        data =json.dumps({
            "email":'admin@admin.com',
            "password": "123456"
    }),
    content_type="application/json")

    if loginAdmin.status_code == 200:
        tokenAdmin = loginAdmin.get_json()["token"]

    loginUser = client.post('/autentication/login', 
        data =json.dumps({
            "email":'joao.ponciano@email.com',
            "password": "123456"
    }),
    content_type="application/json")

    
    if loginUser.status_code == 200:
        tokenUser = loginUser.get_json()["token"]
        userId = loginUser.get_json()["user"]['id']

    #Tenatando acessar a area vip sem permissão
    areaVipNotPermission = client.get('/vip/livros', headers={"Authorization": "Bearer {}".format(tokenUser)})
    
    #Consedendo acesso a area vip atraves do admin
    setVip = client.put('/admin/editRole/'+userId,data=json.dumps({
        "role":"VIP"
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    #Acessando a area vip sem token
    areaVipNotToken = client.get('/vip/livros')

    #Livros
    #Consultando todos os livros
    areaVipAll = client.get('/vip/livros', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando por filtro de pesquisa
    areaVipSearch = client.get('/vip/livros?search=teste', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando por paginação
    areaVipPage = client.get('/vip/livros?page=2&pageSize=1', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando por tamanho de itens da pagina
    areaVipPageSize = client.get('/vip/livros?pageSize=1', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenado por uma metrica que ão existe
    areaVipOrdering400 = client.get('/vip/livros?ordering=1', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por ano
    areaVipOrderingAno = client.get('/vip/livros?ordering=anoLancamento', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por nome
    areaVipOrderingName = client.get('/vip/livros?ordering=name', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por autor
    areaVipOrderingAutor = client.get('/vip/livros?ordering=autor', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por avaliação
    areaVipOrderingAvaliacao = client.get('/vip/livros?ordering=avaliacao', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando por avaliação
    areaVipAssessment = client.get('/vip/livros?assessment=5', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Adicionando um livro para consultalo pelo id posteriormente
    addLivroAdmin = client.post('/admin/addLivro',
    data=json.dumps({
        "nome": "Filme com o id",
        "autor": "Gabriel Oliveira",
        "avaliacao":5,
        "anoLancamento": 1987
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")

    if addLivroAdmin.status_code == 201:
        livroid = addLivroAdmin.get_json()['Livro']['id']
    
    areaVipId = client.get('/vip/livros?id='+livroid, headers={"Authorization": "Bearer {}".format(tokenUser)})


    #Series
    #Consultando todas as series
    areaVipAllSeries = client.get('/vip/series', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando por filtro de pesquisa
    areaVipSearchSeries = client.get('/vip/series?search=teste', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando por paginação
    areaVipPageSeries = client.get('/vip/series?page=2&pageSize=1', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando por tamanho de itens da pagina
    areaVipPageSizeSeries = client.get('/vip/series?pageSize=1', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenado por uma metrica que ão existe
    areaVipOrdering400Series = client.get('/vip/series?ordering=1', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por ano
    areaVipOrderingAnoSeries = client.get('/vip/series?ordering=anoLancamento', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por nome
    areaVipOrderingNameSeries = client.get('/vip/series?ordering=name', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por autor
    areaVipOrderingDescricaoSeries = client.get('/vip/series?ordering=descricao', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Ordenando por avaliação
    areaVipOrderingAvaliacaoSeries = client.get('/vip/series?ordering=avaliacao', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Consultando por avaliação
    areaVipAssessmentSeries = client.get('/vip/series?assessment=4', headers={"Authorization": "Bearer {}".format(tokenUser)})

    #Adicionando uma serie para consultala pelo id posteriormente
    addSeriesAdmin = client.post('/admin/addSerie',
    data=json.dumps({
        "nome": "Filme com o id",
        "descricao": "Gabriel Oliveira",
        "avaliacao":5,
        "anoLancamento": 1987
    }),
    headers={"Authorization": "Bearer {}".format(tokenAdmin)},
    content_type="application/json")


    if addSeriesAdmin.status_code == 201:
        serieid = addSeriesAdmin.get_json()['Serie']['id']
    
    areaVipIdSeries = client.get('/vip/series?id='+serieid, headers={"Authorization": "Bearer {}".format(tokenUser)})

    assert areaVipNotPermission.status_code == 403
    assert setVip.status_code == 200
    assert areaVipNotToken.status_code == 400
    assert areaVipAll.status_code == 200
    assert areaVipSearch.status_code == 200
    assert areaVipSearch.get_json()['A.info']['Page size'] < areaVipSearch.get_json()['A.info']['Itens totais']
    assert areaVipPage.status_code == 200
    assert areaVipPage.get_json()['A.info']['Page'] == 2
    assert areaVipPageSize.status_code == 200
    assert areaVipPageSize.get_json()['A.info']['Page size'] == 1
    assert areaVipOrdering400.status_code == 400
    assert areaVipOrderingAno.status_code ==200
    assert areaVipOrderingName.status_code ==200
    assert areaVipOrderingAutor.status_code ==200
    assert areaVipOrderingAvaliacao.status_code ==200
    assert areaVipAssessment.status_code == 200
    assert areaVipAssessment.get_json()['A.info']['Page size'] < areaVipAssessment.get_json()['A.info']['Itens totais']
    assert areaVipId.status_code == 200
    assert areaVipId.get_json()['Livro']['id'] == livroid
    assert areaVipAllSeries.status_code == 200
    assert areaVipSearchSeries.status_code == 200
    assert areaVipSearchSeries.get_json()['A.info']['Page size'] < areaVipSearchSeries.get_json()['A.info']['Itens totais']
    assert areaVipPageSeries.status_code == 200
    assert areaVipPageSeries.get_json()['A.info']['Page'] == 2
    assert areaVipPageSizeSeries.status_code == 200
    assert areaVipPageSizeSeries.get_json()['A.info']['Page size'] == 1
    assert areaVipOrdering400Series.status_code == 400
    assert areaVipOrderingAnoSeries.status_code ==200
    assert areaVipOrderingNameSeries.status_code ==200
    assert areaVipOrderingDescricaoSeries.status_code ==200
    assert areaVipOrderingAvaliacaoSeries.status_code ==200
    assert areaVipAssessmentSeries.status_code == 200
    assert areaVipAssessmentSeries.get_json()['A.info']['Page size'] < areaVipAssessmentSeries.get_json()['A.info']['Itens totais']
    assert areaVipIdSeries.status_code == 200
    assert areaVipIdSeries.get_json()['Serie']['id'] == serieid