import { AuthContext } from '../contexts/auth';
import { useState, useEffect, useContext } from "react";
import axios from 'axios';
import NavBar from '../componentes/NavBar';
import './styles/Livros.css'

function Livros(){

    const authContext = useContext(AuthContext);
    const userToken = authContext.token;
    const userRole = authContext.role;

    const [livros, setLivros] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);

    useEffect(() => {
        previewLivro();
    }, [currentPage]);

    async function previewLivro() {
            if (userRole === 2 || userRole === 3) {
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
        } else {
        console.log('Usuário não tem permissão para acessar informações de livros.');
        }
    }

    const LivroList = livros.map((livro) => (
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
                <h1 className='title'>Livros</h1>

               <br></br>

                {userRole === 2 || userRole === 3 ? (
                    <div className='livro-container'>
                      {LivroList}
                    </div>
                  ) : (
                    <div className='livro-empty-list-container'>
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
                        className={`pagination-button ${livros.length === 0 ? 'disabled' : ''}`}
                        disabled={livros.length === 0}
                        onClick={handleNextPage}
                    >
                        Próxima
                    </button>
                </div>
            </div>

        </div>
    )

    

}

export default Livros