import { AuthContext } from '../contexts/auth';
import { useState, useEffect, useContext } from "react";
import axios from 'axios';

import './styles/Filmes.css'
import NavBar from '../componentes/NavBar';

function Filmes() {
    const authContext = useContext(AuthContext);
    const userToken = authContext.token;

    const [filmes, setFilmes] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages] = useState(0);

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
        <div className="container">
            <div className='container-navBar'>
                <span className="logo">
                    <img
                        src="https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png"
                        alt="Cabypa software"
                    />
                </span>
                <NavBar userToken={userToken} />
            </div>

            <div className='preview'>
                <h1 className='title'>Filmes</h1>

               
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
                        className={`pagination-button ${currentPage === totalPages || filmes.length === 0 ? 'disabled' : ''}`}
                        disabled={currentPage === totalPages || filmes.length === 0}
                        onClick={handleNextPage}
                    >
                        Próxima
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Filmes;
