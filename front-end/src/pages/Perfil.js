import { AuthContext } from '../contexts/auth';
import { useState, useEffect, useContext } from "react";
import axios from 'axios';
import NavBar from '../componentes/NavBar';
import './styles/Perfil.css';
import { format, parseISO } from 'date-fns';
import moment from 'moment';

function Perfil() {
  const authContext = useContext(AuthContext);
  const userId = authContext.id; // Acessando o ID do usuário do contexto
  const userToken = authContext.token;

  const [img, setImg] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [nascimento, setNascimento] = useState('');
  const [phone, setPhone] = useState('');
  const [cpf, setCpf] = useState('');
  const [role, setRole] = useState('');

  const [editing, setEditing] = useState(false);

  useEffect(() => {
    getPerfil();
  }, []);

  async function getPerfil() {
    const options = {
      method: 'GET',
      url: `http://localhost:5000/admin/user/${userId}`,
      headers: {
        Authorization: `Bearer ${userToken}`,
      },
    };

    try {
      const response = await axios(options);
      setImg(response.data.Img.img);
      setEmail(response.data.User.email);
      setName(response.data.User.name);
      setPhone(response.data.User.phone);
      const data = moment(response.data.User.birth_date).add(1, 'days');
      setNascimento(data.format('DD/MM/YYYY'));
      setCpf(response.data.User.cpf);
      if (response.data.User.role === 1) {
        setRole('Não é vip');
      } else if (response.data.User.role === 2) {
        setRole('Vip');
      } else {
        setRole('Admin');
      }
    } catch (error) {
      console.log('Erro ao pegar perfil');
    }
  }

  function formatDate(date) {
    const formattedDate = parseISO(date);
    return format(formattedDate, 'dd/MM/yyyy');
  }
  
  async function handleUpdateProfile(e) {
    e.preventDefault();
    
    const body = {
      name: name,
      cpf: cpf,
      phone: phone,
      birth_date: formatDate(nascimento).toString(),
    };

    try {
      const options = {
        method: 'PUT',
        url: `http://localhost:5000/user/updateProfile`,
        headers: {
          Authorization: `Bearer ${userToken}`,
        },
        data: body,
      };
      console.log(body)
      const response = await axios(options);
      console.log(response.data);
    } catch (error) {
      console.log('Erro ao atualizar perfil');
    }
    

    setEditing(false);
  }

  return (
    <div className="container">
      <div className="container-navBar">
        <span className="logo">
          <img
            src="https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png"
            alt="Cabypa software"
          />
        </span>
        <NavBar userToken={userToken} />
      </div>

      <div className="warp-perfil">
        <h1 className="title">Meu Perfil</h1>
        <br></br>

        <span className="perfil">
          <img src={`data:image/jpeg;base64, ${img}`} alt="Perfil" />
        </span>

        <div className="informacoes">
          <h2>Informações:</h2>
          {editing ? (
            <form onSubmit={handleUpdateProfile}>
              <label>
                Nome:
                <input
                  className="input"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
                <span className="focus-input"></span>
              </label>
              <label>
                Data de Nascimento:
                <input
                  className="input"
                  type="date"
                  value={nascimento}
                  onChange={(e) => setNascimento(e.target.value)}
                />
                <span className="focus-input"></span>
              </label>
              <label>
                Telefone:
                <input
                  className="input"
                  type="string"
                  value={phone}
                  onChange={(e) =>{console.log(e.target.value); setPhone(e.target.value)}}
                />
                <span className="focus-input"></span>
              </label>
              <label>
                CPF:
                <input
                  className="input"
                  type="string"
                  value={cpf}
                  onChange={(e) =>{console.log(e.target.value); setCpf(e.target.value)}} 
                />
                <span className="focus-input"></span>
              </label>
              <button className="button-perfil" type="submit">
                Salvar
              </button>
            </form>
          ) : (
            <>
              <p>
                <strong>Nome:</strong> {name ? name : "Não informado"}
              </p>
              <p>
                <strong>Email:</strong> {email ? email : "Não informado"}
              </p>
              <p>
                <strong>Data de Nascimento:</strong>{" "}
                {nascimento ? nascimento : "Não informado"}
              </p>
              <p>
                <strong>Telefone:</strong> {phone ? phone : "Não informado"}
              </p>
              <p>
                <strong>CPF:</strong> {cpf ? cpf : "Não informado"}
              </p>
              <p>
                <strong>Plano:</strong> {role ? role : "Não informado"}
              </p>
              <button
                className="button-perfil"
                onClick={() => setEditing(true)}
              >
                Editar Perfil
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Perfil;
