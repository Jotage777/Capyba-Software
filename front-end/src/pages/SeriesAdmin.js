import { AuthContext } from '../contexts/auth';
import { useState, useEffect, useContext } from "react";
import axios from 'axios';
import NavBarAdmin from '../componentes/NavBArAdmin'

import'./styles/SeriesAdmin.css'


function SeriesAdmin(){
    const authContext = useContext(AuthContext);
    const userToken = authContext.token;

    const [series, setSeries] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [adicionar, setAdicionar] = useState(false);

    const [name, setName] = useState('');
    const [descricao, setDescricao] = useState('');
    const [avaliacao,setAvaliacao] = useState('')
    const [anoLancamento,setAnoLancamento] = useState('')

    useEffect(() => {
        async function previewSeries() {
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
    }
        previewSeries();
    }, [currentPage,userToken]);


    async function addSerie(e){
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
              url: `http://localhost:5000/admin/addSerie`,
              headers: {
                Authorization: `Bearer ${userToken}`,
            },
              data: body,
            };

            await axios(options);
            alert ('Serie adicionado com sucesso!')
        } catch (error) {
            alert ('Erro á adicionar a Serie!')
        }

        setAdicionar(false)

    }

    const seriesList = series.map((serie) => (
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

    const handleAvaliacaoChange = (e) => {
        const valor = e.target.value;
        const avaliacaoInt = parseInt(valor, 10);
    
        if (avaliacaoInt >= 1 && avaliacaoInt <= 5) {
          setAvaliacao(avaliacaoInt.toString());
        } else {
          setAvaliacao('');
        }
    };
    
    const handleAnoLancamentoChange = (e) => {
        const valor = e.target.value;
        const anoAtual = new Date().getFullYear();
        const anoLancamentoInt = parseInt(valor, 10);
    
        if (anoLancamentoInt <= anoAtual) {
          setAnoLancamento(anoLancamentoInt.toString());
        } else {
          setAnoLancamento('');
        }
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

                <h1 className='title'>Séries</h1>

                {adicionar ? (
                    <form className='form-add-serie' onSubmit={addSerie}>
                        <h1>Adicionar Série</h1>
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
                            onChange={handleAnoLancamentoChange}
                            />
                            <span className="focus-input"></span>
                        </label>

                        <label>
                            Avaliação:
                            <input
                            className="input"
                            type="number"
                            value={avaliacao}
                            onChange={handleAvaliacaoChange}
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
                        <button className="button-add-serie" type="submit">
                            Adicionar
                        </button>
                    </form>
                ):(
                    <>
                        <br></br>

                        <button className='adicionar' onClick={() => setAdicionar(true)}> Adicionar Serie</button>
        
                        <br></br>
        
                        <div className='serie-container'>
                            {seriesList}
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
                                className={`pagination-button ${series.length < 9 ? 'disabled' : ''}`}
                                disabled={series.length === 0}
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

export default SeriesAdmin