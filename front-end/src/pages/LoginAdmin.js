import styles from './styles/Login.module.css'
import { useState } from "react";
import axios from 'axios'

function LoginAdmin(){

    async function loginApi(email, password){
        const body = {
            email: email,
            password: password
        }
        const options ={
            method: 'POST',
            data: body,
            url: "http://localhost:5000/autentication/login"
        }
        try{
            await axios(options)
            console.log('Deu certo')
        }catch{
            console.log('deu erro')
        }
        
    }

    const [email, setEmail] =useState()
    const [password, setPassword] =useState()
    return(
        <div className={styles.container}>
            <div className={styles.container_login}>
                <div className={styles.warp_login}>
                    <form className="login-form">
                        
                        <span className={styles.login_form_title}>Área do Admin</span>

                        <br></br>

                        <span className={styles.logo}>
                            <img src = "https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png" alt="Cabypa software"/>
                        </span>

                        <br></br>
                        <br></br>


                        <div className={styles.Autenticacao}>
                            <input className={styles.input} 
                                type="email"
                                placeholder="Email"
                                value ={email}
                                onChange={e => setEmail(e.target.value)}
                            />
                            <span className={styles.focus_input} ></span>
                        </div>

                        <div className={styles.Autenticacao}>
                            <input className={styles.input} 
                                type="password"
                                placeholder="Senha"
                                value ={password}
                                onChange={e => setPassword(e.target.value)}
                            />
                            <span className={styles.focus_input} ></span>
                        </div>

                     

                        <div className={styles.container_login_form_btn}>
                            <button className={styles.button_login} onClick={()=>loginApi(email, password)}>Login</button>
                        </div>


                      
                    </form>
                </div>

            </div>


        </div>
    )
}

export default LoginAdmin