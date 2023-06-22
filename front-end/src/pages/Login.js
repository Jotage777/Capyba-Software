import styles from './styles/Login.module.css'
import { useState } from "react";

function Login(){

    const [email, setEmail] =useState()
    const [password, setPassword] =useState()
    return(
        <div className={styles.container}>
            <div className={styles.container_login}>
                <div className={styles.warp_login}>
                    <form className="login-form">
                        
                        <spam className={styles.login_form_title}>Bem vindo</spam>

                        <br></br>

                        <spam className={styles.logo}>
                            <img src = "https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png" alt="Cabypa software"/>
                        </spam>

                        <br></br>
                        <br></br>


                        <div className={styles.Autenticacao}>
                            <input className={styles.input} 
                                type="email"
                                value ={email}
                                onChange={e => setEmail(e.target.value)}
                            />
                            <span className={styles.focus_input} data-placeholder="Email"></span>
                        </div>

                        <div className={styles.Autenticacao}>
                            <input className={styles.input} 
                                type="password"
                                value ={password}
                                onChange={e => setPassword(e.target.value)}
                            />
                            <span className={styles.focus_input} data-placeholder="Senha"></span>
                        </div>

                     

                        <div className={styles.container_login_form_btn}>
                            <button className={styles.button_login}>Login</button>
                        </div>


                        <div className={styles.cadastro_link}>
                            <span className={styles.txt1}>Não possui conta?</span>
                            <a className={styles.txt2} href="/pagina-de-cadastro">
                                Cadastrar-se
                            </a>
                        </div>
                    </form>
                </div>

            </div>


        </div>
    )
}

export default Login