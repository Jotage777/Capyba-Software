import { Link } from "react-router-dom";
import './styles/NavBar.css'
function NavBar(){
    return (
        <div className="all">
            <div className="categorias">
                <Link>Filmes</Link>
                <Link>Series</Link>
                <Link>Livros</Link>
                <Link>Meu perfil</Link>
                <Link>Sair</Link>
            </div>
            
        </div>
        
    )
}

export default NavBar