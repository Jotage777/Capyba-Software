import { AuthContext } from '../contexts/auth';
import { useState, useEffect, useContext } from "react";
import axios from 'axios';
import NavBarAdmin from '../componentes/NavBArAdmin'

import './styles/FilmesAdmin.css'

function FilmesAdmin(){
    const authContext = useContext(AuthContext);
    const userToken = authContext.token;

    const [filmes, setFilmes] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [adicionar, setAdicionar] = useState(false);
    const [name, setName] = useState('');
    const [descricao, setDescricao] = useState('');
    const [avaliacao,setAvaliacao] = useState('')
    const [anoLancamento,setAnoLancamento] = useState('')

    useEffect(() => {
        previewFilmes();
    }, [currentPage]);

    async function previewFilmes() {
        const options = {
            method: 'GET',
            url: `http://localhost:5000/public/filmes?page=${currentPage}&pageSize=9`,
            headers: {
                Authorization: `Bearer ${userToken}`,
            },
        };

        try {
            const response = await axios(options);
            const filmesData = response.data.Filmes;
            setFilmes(filmesData);
            
        } catch (error) {
            setFilmes([]);
        }
    }

    async function addFilme(e){
        e.preventDefault();

        const body = {
            nome: name,
            descricao: descricao,
            avaliacao:avaliacao,
            anoLancamento: anoLancamento
        }

        try {
            const options = {
              method: 'POST',
              url: `http://localhost:5000/admin/addFilme`,
              headers: {
                Authorization: `Bearer ${userToken}`,
            },
              data: body,
            };

            await axios(options);
            alert ('Filme adicionado com sucesso!')
        } catch (error) {
            alert ('Erro á adicionar o filme!')
        }

        setAdicionar(false)

    }

    const filmesList = filmes.map((filme) => (
        <div key={filme.id} className="filme">
            <h3 className="filme-title">{filme.name} <br /></h3>
            <p className="filme-info">Ano de Lançamento: <br />{filme.anoLancamento} <br /></p>
            <p className="filme-info">Avaliação: <br />{filme.avaliacao} <br /></p>
            <p className="filme-info">Descrição: <br />{filme.descricao} <br /></p>
        </div>
    ));

    const handlePreviousPage = () => {
        setCurrentPage((prevPage) => prevPage - 1);
    };

    const handleNextPage = () => {
        setCurrentPage((prevPage) => prevPage + 1);
    };

    return (
        <div className='container'>
            <div className='container-navBar'>
                  <span className="logo">
                  <img
                      src="https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png"
                      alt="Cabypa software"
                  />
                  </span>
                  <NavBarAdmin userToken={userToken}/>
            </div>

            <div className='preview'>

                <h1 className='title'>Filmes</h1>

                {adicionar ? (
                    <form className='form-add-filme' onSubmit={addFilme}>
                        <h1>Adicionar Filme</h1>
                        <br></br>
                        <label>
                            Nome:
                            <input
                            className="input"
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            />
                            <span className="focus-input"></span>
                        </label>

                        <label>
                            Ano de lançamento:
                            <input
                            className="input"
                            type="number"
                            value={anoLancamento}
                            onChange={(e) => setAnoLancamento(e.target.value)}
                            />
                            <span className="focus-input"></span>
                        </label>

                        <label>
                            Avaliação:
                            <input
                            className="input"
                            type="number"
                            value={avaliacao}
                            onChange={(e) => setAvaliacao(e.target.value)}
                            />
                            <span className="focus-input"></span>
                        </label>

                        <label>
                            Descrição:
                            <input
                            className="input"
                            type="text"
                            value={descricao}
                            onChange={(e) => setDescricao(e.target.value)}
                            />
                            <span className="focus-input"></span>
                        </label>
                        <br></br>
                        <button className="button-add-filme" type="submit">
                            Adicionar
                        </button>
                    </form>
                ):(
                    <>
                        <br></br>

                        <button className='adicionar' onClick={() => setAdicionar(true)}> Adicionar Filme</button>
        
                        <br></br>
        
                        <div className='filmes-container'>
                            {filmesList}
                        </div>
        
                        <br />
        
                        <div className="pagination">
                            <button
                                className={`pagination-button ${currentPage === 1 ? 'disabled' : ''}`}
                                disabled={currentPage === 1}
                                onClick={handlePreviousPage}
                            >
                                Anterior
                            </button>
                            <span className="pagination-info">
                                Página {currentPage} 
                            </span>
                            <button
                                className={`pagination-button ${filmes.length < 9 ? 'disabled' : ''}`}
                                disabled={filmes.length === 0}
                                onClick={handleNextPage}
                            >
                                Próxima
                            </button>
                        </div>
                    </>
                )}

              
            </div>

        </div>
    )
}

export default FilmesAdmin