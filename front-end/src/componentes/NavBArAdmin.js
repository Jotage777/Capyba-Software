import { Link } from "react-router-dom";
import axios from 'axios'
import './styles/NavBar.css'

function NavBArAdmin({ userToken }){

    async function logout(){
        const options = {
            method: 'POST',
            url: 'http://localhost:5000/autentication/logout',
            headers: {
                Authorization: `Bearer ${userToken}`,
            },
            };
    
            try {
            await axios(options);
            alert('Volte sempre')
            } catch (error) {
            alert('erro a realizar o logout')
            }
    }

    return (
        <div className="all">
            <div className="categorias">
                <Link to='/admin/home'>Home</Link>
                <Link to='/admin/filmes'>Filmes</Link>
                <Link to='/admin/series'>Séries</Link>
                <Link to='/admin/livros'>Livros</Link>
                <Link to='/admin/usuarios'>Usuários</Link>
                <Link to='/admin/login' onClick={logout}>Sair</Link>
            </div>
            
        </div>
        
    )

}

export default NavBArAdmin