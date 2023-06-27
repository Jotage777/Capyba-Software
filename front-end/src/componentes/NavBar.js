import { Link } from "react-router-dom";
import axios from 'axios'
import './styles/NavBar.css'

function NavBar({ userToken }){

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
                <Link to='/home'>Home</Link>
                <Link to='/filmes'>Filmes</Link>
                <Link to='/series'>Séries</Link>
                <Link to='/livros'>Livros</Link>
                <Link to='/perfil'>Meu perfil</Link>
                <Link to='/' onClick={logout}>Sair</Link>
            </div>
            
        </div>
        
    )
}

export default NavBar