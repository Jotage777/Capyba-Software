import { AuthContext } from '../contexts/auth';
import { useState, useEffect, useContext } from "react";
import axios from 'axios'

import './styles/Home.css'
import NavBar from '../componentes/NavBar';

function Home() {
    const authContext = useContext(AuthContext);
    const userId = authContext.id; // Acessando o ID do usuário do contexto
    const userToken = authContext.token;
    const username = authContext.username;
    const userRole = authContext.role;

    const [filmes, setFilmes] = useState([]);
    const [livros, setLivros] = useState([]);
    const [series, setSeries] = useState([]);

    useEffect(() => {
        previewFilmes();
        previewSeries();
        previewLivro();
    }, []);

    async function previewFilmes() {
        const options = {
        method: 'GET',
        url: 'http://localhost:5000/public/filmes',
        headers: {
            Authorization: `Bearer ${userToken}`,
        },
        };

        try {
        const response = await axios(options);
        const filmesData = response.data.Filmes;
        setFilmes(filmesData);
        } catch (error) {
        console.log('Erro ao obter filmes:', error);
        }
    }

    async function previewSeries() {
        if (userRole === 2 || userRole === 3) {
          try {
            const response = await axios.get('http://localhost:5000/vip/series', {
              headers: {
                Authorization: `Bearer ${userToken}`,
              },
            });
            const seriesData = response.data.Series;
            setSeries(seriesData);
          } catch (error) {
            console.log('Erro ao obter séries:', error);
          }
        } else {
          console.log('Usuário não tem permissão para acessar informações de séries.');
        }
      }
    
      async function previewLivro() {
        if (userRole === 2 || userRole === 3) {
          try {
            const response = await axios.get('http://localhost:5000/vip/livros', {
              headers: {
                Authorization: `Bearer ${userToken}`,
              },
            });
            const livrosData = response.data.Livros;
            setLivros(livrosData);
          } catch (error) {
            console.log('Erro ao obter livros:', error);
          }
        } else {
          console.log('Usuário não tem permissão para acessar informações de livros.');
        }
      }

    const filmesList = filmes.map((filme) => (
        <div key={filme.id} className="filme">
        <h3 className="home-title">{filme.name} <br></br> </h3>
        <p className="home-info">Ano de Lançamento: <br></br>{filme.anoLancamento} <br></br> </p>
        <p className="home-info">Avaliação: <br></br>{filme.avaliacao} <br></br> </p>
        <p className="home-info">Descrição: <br></br>{filme.descricao} <br></br> </p>
        </div>
    ));

    const LivroList = livros.map((livro) => (
        <div key={livro.id} className="filme">
        <h3 className="home-title">{livro.name} </h3>
        <p className="home-info">Ano de Lançamento: <br></br>{livro.anoLancamento} </p>
        <p className="home-info">Avaliação: <br></br>{livro.avaliacao} </p>
        <p className="home-info">Autor: <br></br>{livro.autor} </p>
        </div>
    ));

    const SeriesList = series.map((serie) => (
        <div key={serie.id} className="filme">
        <h3 className="home-title">{serie.name} <br></br> </h3>
        <p className="home-info">Ano de Lançamento: <br></br> {serie.anoLancamento} <br></br> </p>
        <p className="home-info">Avaliação: <br></br>{serie.avaliacao} <br></br> </p>
        <p className="home-info">Descrição: <br></br>{serie.descricao} <br></br> </p>
        </div>
    ));

    return (
        <div className="container">
          <div className='container-bem-vindo'>
                  <div className='bem-vindo'>
                  Olá, {username}. Seja bem-vindo!
                  </div>
          </div>

          <div className='container-navBar'>
                  <span className="logo">
                  <img
                      src="https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png"
                      alt="Cabypa software"
                  />
                  </span>
                  <NavBar userToken={userToken}/>
          </div>

          <div className='preview'>
                  <h1 className='title'>Filmes, Livros e Séries</h1>
                  
                  <br></br>

                  <h2>Filmes</h2>
                  
                  
                  <div className='home-container'>
                      {filmesList}
                  </div>

                  <br></br>

                  <h2>Livros</h2>

                  {userRole === 2 || userRole === 3 ? (
                    <div className='home-container'>
                      {LivroList}
                    </div>
                  ) : (
                    <div className='empty-list-container'>
                      <img src= 'https://a-static.mlcdn.com.br/450x450/kit-5-placas-de-aviso-espaco-reservado-solicite-permissao-mago-das-camisas/magodascamisas3/15990448327/5869c3a19f47ab9b5fe8ed0ad087bff9.jpeg' alt='Permissão' />
                    </div>
                  )}

                  
                  <br></br>

                  <h2>Series</h2>
                  {userRole === 2 || userRole === 3 ? (
                    <div className='home-container'>
                      {SeriesList}
                    </div>
                  ) : (
                    <div className='empty-list-container'>
                      <img src= 'https://a-static.mlcdn.com.br/450x450/kit-5-placas-de-aviso-espaco-reservado-solicite-permissao-mago-das-camisas/magodascamisas3/15990448327/5869c3a19f47ab9b5fe8ed0ad087bff9.jpeg' alt='Permissão' />
                    </div>
                  )}

                  <br></br>

            </div>
        </div>
  );
}

export default Home;