import { AuthContext } from '../contexts/auth';
import { useState, useEffect, useContext } from "react";
import axios from 'axios';
import NavBarAdmin from '../componentes/NavBArAdmin'
import './styles/UsersAdmin.css'

function UsersAdmin(){

    const authContext = useContext(AuthContext);
    const userToken = authContext.token;

    const [users, setUser] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);

    useEffect(() => {
        const previewUsers = async () => {
            const options = {
                method: 'GET',
                url: `http://localhost:5000/admin/user?page=${currentPage}&pageSize=10`,
                headers: {
                    Authorization: `Bearer ${userToken}`,
                },
            };
    
            try {
                const response = await axios(options);
                const userData = response.data.Users;
                setUser(userData);
            } catch (error) {
                setUser([]);
            }
        };
    
        previewUsers();
    }, [currentPage, userToken]);

    async function vipOrNotVip(id,role){
        const body = {
            role: role
        }

        const options = {
            method: 'PUT',
            url: `http://localhost:5000/admin/editRole/${id}`,
            headers: {
                Authorization: `Bearer ${userToken}`,
            },
            data:body
        };

        try {
            await axios(options);
            alert('Role do usuário mudado com sucesso!')
        } catch (error) {
            alert('Erro para mudar o role do usuario!')
        }

    }

    const usersList = users
    .filter((user) => user.role !== 3) // Filtra apenas os usuários cujo role não seja igual a 3
    .map((user) => (
        <div key={user.id} className="user">
            <div className="user-info">
                <div className="user-details">
                <h3 className="user-name">Nome: {user.name}</h3>
                <p className="user-email">Email: {user.email}</p>
                <p className="user-cpf">CPF: {user.cpf}</p>
                <p className="user-phone">Telefone: {user.phone}</p>
                <p className="user-role">Função: {user.role}</p>
                <p className="user-id">ID: {user.id}</p>
                </div>
                <div className="user-buttons-container">
                <button className="edit-button" onClick={()=> vipOrNotVip(user.id,'VIP')}>Tornar Vip</button>
                <button className="delete-button" onClick={()=> vipOrNotVip(user.id,'PUBLIC')}>Tornar Comum</button>
                </div>
            </div>
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
                <h1 className='title'>Usuários</h1>

                <br></br>

                <div className='users-container'>
                    {usersList}
                </div>

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
                        className={`pagination-button ${users.length < 10 ? 'disabled' : ''}`}
                        disabled={users.length < 9}
                        onClick={handleNextPage}
                    >
                        Próxima
                    </button>
                </div>
        


            </div>

        </div>
    )

}

export default UsersAdmin