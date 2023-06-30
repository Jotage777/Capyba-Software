import './styles/ConfirmarConta.css'
import { useState, useEffect, useContext } from "react";
import { AuthContext } from '../contexts/auth';
import axios from 'axios'
import { useNavigate } from 'react-router-dom';

function ConfirmarConta(navigate){
    const authContext = useContext(AuthContext);
    const userId = authContext.id; // Acessando o ID do usuário do contexto

    const [code, setCode] = useState('');
    const [showLink, setShowLink] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
          setShowLink(true);
        }, 30000);
    
        return () => clearTimeout(timer);
      }, []);

    async function confirmar(e){
        e.preventDefault();

        const body ={
            code: code
        }

        const options = {
            method: 'POST',
            data:body,
            url: 'http://localhost:5000/user/confirmedCode/'+userId
            
        };
        try{
            await axios(options);
            alert('Conta confirmada');
            navigate('/');
        }catch (error){
            alert(`Erro:${error}`);
        }

    }

    async function reenviarCodigo(){
        const options = {
            method: 'POST',
            url: 'http://localhost:5000/user/resendCode/'+userId
            
        };
        try{
            await axios(options);
            alert('Códifo reenviado');
        }catch (error){
            alert(`Erro:${error}`);
        }

    }
    return (
        <div className="container">
            <div className="container-confirmar-conta">
                <div className="warp-confirmar-conta">
                    <form className="confirmar-conta-form">
                        <span className="title">Confirmação de conta</span>

                        <br></br>

                        <span className='logo'>
                            <img src = "https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png" alt="Cabypa software"/>
                        </span>
                        
                        <br></br>
                        <br></br>

                        <div className='confirmar-code'>
                            <input className='input' 
                                type="string"
                                placeholder="Codigo de confirmação"
                                value ={code}
                                onChange={e => setCode(e.target.value)}
                            />
                            <span className='focus-input' ></span>
                            
                        </div>

                        {showLink && (
                            // eslint-disable-next-line
                            <a onClick={reenviarCodigo}>Reenviar código de confirmação!</a>
                        )}

                        <br></br>
                        <br></br>
                        
                        <button className='button-confirmar-code' onClick={(e) => confirmar(e)}>Confirmar</button>

                       
                    </form>
                </div>
            </div>
        </div>
    )
}

export default ConfirmarConta