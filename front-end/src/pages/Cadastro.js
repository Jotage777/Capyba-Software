import './styles/Cadastro.css'
import { useState } from "react";
import axios from 'axios'

function Cadastro (){
    const [nome, setNome] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [imagem, setImagem] = useState(null);

    async function cadastrar(e){
        
        e.preventDefault()

        console.log(nome)
        console.log(email)
        console.log(password)
        console.log(imagem)

        const formData = new FormData();
        formData.append('name', nome);
        formData.append('email', email);
        formData.append('password', password);
        formData.append('imagem', imagem);

        console.log(formData)
        

        const options = {
            method: 'POST',
            data: formData,
            url: 'http://localhost:5000/user/register'
            
        };
        
        try {
            const response = await axios(options);
            console.log('Resposta:', response.data); // Exemplo de como lidar com a resposta
            alert('Resposta:', response.data);
        } catch (error) {
            console.error('Erro:', error); // Exemplo de como lidar com o erro
            alert(`Erro:${error}`);
        }
        
    }
    
    return (
        <div className='container'>
            <div className='container-cadastro'>
                <div className='warp-cadastro'>
                    <form enctype="multipart/form-data" className='cadastro-form'>
                        <span className='title'>Cadastro de usuários</span>

                            <br></br>

                            <span className='logo'>
                                <img src = "https://ecossistema.pe/wp-content/uploads/listing-uploads/logo/2020/11/capyba_simbolo_colorido-1.png" alt="Cabypa software"/>
                            </span>

                            <br></br>
                            <br></br>

                            <div className='cadastro'>
                                <input className='input' 
                                    type="string"
                                    placeholder="Nome"
                                    value ={nome}
                                    onChange={e => setNome(e.target.value)}
                                />
                                <span className='focus-input' ></span>
                            </div>

                            <div className='cadastro'>
                                <input className='input' 
                                    type="email"
                                    placeholder="Email"
                                    value ={email}
                                    onChange={e => setEmail(e.target.value)}
                                />
                                <span className='focus-input' ></span>
                            </div>

                            <div className='cadastro'>
                                <input className='input' 
                                    type="password"
                                    placeholder="Senha"
                                    value ={password}
                                    onChange={e => setPassword(e.target.value)}
                                />
                                <span className='focus-input' ></span>
                            </div>

                            <div className='cadastro-img'>
                                <label>Enviar imagem(perfil):</label>
                                <br></br>
                                <br></br>
                                <input className='input' 
                                    type="file"
                                    name="imagem"
                                    onChange={e => {
                                        if (e.target.files.length > 0) {
                                          setImagem(e.target.files[0]);
                                        }
                                      }}
                                />
                            </div>

                            <button className='button-cadastro' onClick={(e) => cadastrar(e)}>Cadastrar</button>


                        </form>
                </div>

            </div>

        </div>
    )
}

export default Cadastro