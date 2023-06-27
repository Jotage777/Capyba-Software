import { AuthContext } from '../contexts/auth';
import { useState, useEffect, useContext } from "react";
import axios from 'axios';
import NavBar from '../componentes/NavBar';
import './styles/Series.css'

function Series(){

    const authContext = useContext(AuthContext);
    const userToken = authContext.token;
    const userRole = authContext.role;

    const [series, setSeries] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);


    useEffect(() => {
        previewSeries();
    }, [currentPage]);

    async function previewSeries() {
        if (userRole === 2 || userRole === 3) {
            try {
                const options = {
                    method: 'GET',
                    url: `http://localhost:5000/vip/series?page=${currentPage}&pageSize=9`,
                    headers: {
                        Authorization: `Bearer ${userToken}`,
                    },
                };
                
               
                const response = await axios(options);
                const seriesData = response.data.Series;
                setSeries(seriesData);
                
            } catch (error) {
                setSeries([]);
            }
        } else {
        console.log('Usuário não tem permissão para acessar informações de livros.');
        }
    }

    const SeriesList = series.map((serie) => (
        <div key={serie.id} className="serie">
        <h3 className="serie-title">{serie.name} <br></br> </h3>
        <p className="serie-info">Ano de Lançamento: <br></br> {serie.anoLancamento} <br></br> </p>
        <p className="serie-info">Avaliação: <br></br>{serie.avaliacao} <br></br> </p>
        <p className="serie-info">Descrição: <br></br>{serie.descricao} <br></br> </p>
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
                <NavBar userToken={userToken} />
            </div>

            <div className='preview'>
                <h1 className='title'>Séries</h1>

               <br></br>

                {userRole === 2 || userRole === 3 ? (
                    <div className='serie-container'>
                      {SeriesList}
                    </div>
                  ) : (
                    <div className='serie-empty-list-container'>
                      <img src= 'https://a-static.mlcdn.com.br/450x450/kit-5-placas-de-aviso-espaco-reservado-solicite-permissao-mago-das-camisas/magodascamisas3/15990448327/5869c3a19f47ab9b5fe8ed0ad087bff9.jpeg' alt='Permissão' />
                    </div>
                  )}


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
                        className={`pagination-button ${series.length === 0 ? 'disabled' : ''}`}
                        disabled={series.length === 0}
                        onClick={handleNextPage}
                    >
                        Próxima
                    </button>
                </div>
            </div>
        </div>
    )

}

export default Series