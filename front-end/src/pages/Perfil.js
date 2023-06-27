import { AuthContext } from '../contexts/auth';
import { useState, useEffect, useContext } from "react";
import axios from 'axios'
import NavBar from '../componentes/NavBar';


function Perfil(){
    const authContext = useContext(AuthContext);
    const userId = authContext.id; // Acessando o ID do usuário do contexto
    const userToken = authContext.token;

    const [perfil,setPerfil] = useState([])

    async function getPerfil(){
        const options = {
            method: 'GET',
            url: `http://localhost:5000/admin/user/${userId}`,
            headers: {
                Authorization: `Bearer ${userToken}`,
            },
        };

        try {
            const response = await axios(options);
            const userPerfil = response.data.User;
            setPerfil(userPerfil);
            
        } catch (error) {
           console.log('Erro ao pegar perfil')
        }
    }

    return (
        <div className='container'>

            <div className='container-navBar'>
                  <span className="logo">
                  <img
                      src="https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png"
                      alt="Cabypa software"
                  />
                  </span>
                  <NavBar userToken={userToken}/>
            </div>

            <div className='warp-perfil'>
                
            </div>

        </div>
    )

}

export default Perfil;