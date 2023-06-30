import { AuthContext } from '../contexts/auth';
import { useState, useEffect, useContext } from "react";
import axios from 'axios';
import NavBarAdmin from '../componentes/NavBArAdmin'

function LivrosAdmin(){

    const authContext = useContext(AuthContext);
    const userToken = authContext.token;

    const [livros, setLivros] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [adicionar, setAdicionar] = useState(false);

    const [name, setName] = useState('');
    const [autor, setAutor] = useState('');
    const [avaliacao,setAvaliacao] = useState('')
    const [anoLancamento,setAnoLancamento] = useState('')


    useEffect(() => {
        async function previewLivro() {
            try {
                const options = {
                    method: 'GET',
                    url: `http://localhost:5000/vip/livros?page=${currentPage}&pageSize=9`,
                    headers: {
                        Authorization: `Bearer ${userToken}`,
                    },
                };
                
               
                const response = await axios(options);
                const livrosData = response.data.Livros;
                setLivros(livrosData);
                
            } catch (error) {
                setLivros([]);
            }
        }
        previewLivro();
    }, [currentPage, userToken]);

   
    async function addLivro(e){
        e.preventDefault();

        const body = {
            nome: name,
            autor: autor,
            avaliacao:avaliacao,
            anoLancamento: anoLancamento
        }

        try {
            const options = {
              method: 'POST',
              url: `http://localhost:5000/admin/addLivro`,
              headers: {
                Authorization: `Bearer ${userToken}`,
            },
              data: body,
            };

            await axios(options);
            alert ('Livro adicionado com sucesso!')
        } catch (error) {
            alert ('Erro á adicionar o livro!')
        }

        setAdicionar(false)

    }

    const livroList = livros.map((livro) => (
        <div key={livro.id} className="livro">
        <h3 className="livro-title">{livro.name} </h3>
        <p className="livro-info">Ano de Lançamento: <br></br>{livro.anoLancamento} </p>
        <p className="livro-info">Avaliação: <br></br>{livro.avaliacao} </p>
        <p className="livro-info">Autor: <br></br>{livro.autor} </p>
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

                <h1 className='title'>Livros</h1>

                {adicionar ? (
                    <form className='form-add-livro' onSubmit={addLivro}>
                        <h1>Adicionar Livro</h1>
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
                            Autor:
                            <input
                            className="input"
                            type="text"
                            value={autor}
                            onChange={(e) => setAutor(e.target.value)}
                            />
                            <span className="focus-input"></span>
                        </label>
                        <br></br>
                        <button className="button-add-livro" type="submit">
                            Adicionar
                        </button>
                    </form>
                ):(
                    <>
                        <br></br>

                        <button className='adicionar' onClick={() => setAdicionar(true)}> Adicionar Livro</button>
        
                        <br></br>
        
                        <div className='livro-container'>
                            {livroList}
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
                                className={`pagination-button ${livros.length < 9 ? 'disabled' : ''}`}
                                disabled={livros.length < 9}
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

export default LivrosAdmin

