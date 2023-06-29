import { AuthContext } from '../contexts/auth';
import { useContext } from "react";
import './styles/HomeAdmin.css'
import NavBarAdmin from '../componentes/NavBArAdmin'

function HomeAdmin(){
    const authContext = useContext(AuthContext);
    const userToken = authContext.token;

    return (
        <div className="container">
            <div className='container-navBar'>
                  <span className="logo">
                  <img
                      src="https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png"
                      alt="Cabypa software"
                  />
                  </span>
                  <NavBarAdmin userToken={userToken}/>
            </div>

            <div className='preview-admin'>
                <h1 className='title'>Área do admin</h1>

                <br></br>

                <span className='gif'>
                    <img src="https://media.tenor.com/CPudn239v0YAAAAM/leroy-worst-admin.gif" alt="gif admin"/>
                </span>

                <br></br>

                <h2 className='sub-title'>Área reservada apenas para admins</h2>
            </div>

           

        </div>
    )

}

export default HomeAdmin
