import './styles/ConfirmarConta.css'
import { useState } from "react";

function ConfirmarConta(){
    const [code, setCode] = useState('');

    async function confirmar(){

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

                        <button className='button-confirmar-code' onClick={(e) => confirmar(e)}>Confirmar</button>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default ConfirmarConta