import styles from './styles/Login.module.css';
import { useState, useCallback } from "react";
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function loginApi(email, password, onLogin, navigate) {
  return async (e) => {
    e.preventDefault();

    const body = {
      email: email,
      password: password,
    };

    try {
      const response = await axios.post('http://localhost:5000/autentication/login', body);
     
      const userData = {
        id: response.data.user.id,
        token: response.data.token,
        role: response.data.user.role,
        username: response.data.user.name
      };
      onLogin(userData);
      navigate('/home');
      alert('Login realizado com sucesso');
    } catch {
      alert('Deu errado');
    }
  };
}

function Login(props) {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = useCallback(
    loginApi(email, password, props.onLogin, navigate),
    [email, password, props.onLogin, navigate]
  );

  return (
    <div className={styles.container}>
      <div className={styles.container_login}>
        <div className={styles.warp_login}>
          <form className="login-form">
            <span className={styles.login_form_title}>Bem vindo!</span>
            <br />
            <span className={styles.logo}>
              <img src="https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png" alt="Cabypa software" />
            </span>
            <br />
            <br />
            <div className={styles.Autenticacao}>
              <input
                className={styles.input}
                type="email"
                placeholder="Email"
                value={email}
                onChange={e => setEmail(e.target.value)}
              />
              <span className={styles.focus_input}></span>
            </div>
            <div className={styles.Autenticacao}>
              <input
                className={styles.input}
                type="password"
                placeholder="Senha"
                value={password}
                onChange={e => setPassword(e.target.value)}
              />
              <span className={styles.focus_input}></span>
            </div>
            <div className={styles.container_login_form_btn}>
              <button type="submit" className={styles.button_login} onClick={handleLogin}>Login</button>
            </div>
            <div className={styles.cadastro_link}>
              <span className={styles.txt1}>Não possui conta?</span>
              <a className={styles.txt2} href="/cadastro">
                Cadastrar-se
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login;
