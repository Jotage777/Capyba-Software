import { useState } from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Cadastro from './pages/Cadastro';
import ConfirmarConta from './pages/ConfirmarConta';
import LoginAdmin from './pages/LoginAdmin';
import { AuthContext } from './contexts/auth';
import Home from './pages/Home';
import Filmes from './pages/Filmes';
import Livros from './pages/Livros';
import Series from './pages/Series';
import Perfil from './pages/Perfil';
import HomeAdmin from './pages/HomeAdmin';
import FilmesAdmin from './pages/FilmesAdmin';
import SeriesAdmin from './pages/SeriesAdmin';
import LivrosAdmin from './pages/LivrosAdmin';
import UsersAdmin from './pages/UsersAdmin';

function App() {
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
    console.log(userData)
    setUser(userData);
  };

  const handleCadastro = (userData) => {
    setUser(userData);
  };

  return (
    <BrowserRouter>
      <AuthContext.Provider value={user}>
        <Routes>
          <Route path="/" element={<Login onLogin={handleLogin} />} />

          <Route
            path="/cadastro"
            element={<Cadastro onCadastro={handleCadastro} />}
          />

          <Route
            path="/confirmar-conta"
            element={
              user && user.id ? (
                <ConfirmarConta userId={user.id} />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />

          <Route path="/admin/login" element={<LoginAdmin onLogin={handleLogin}/>} />

          <Route path="/home" element={
              user && user.id && user.token && user.username && user.role? (
                <Home userId={user.id} userToken={user.token} username={user.name} userRole={user.role} />
              ) : (
                <Navigate to="/" replace />
              )
            } />

          <Route path="/filmes" element={
            user && user.token ? (
              <Filmes userToken={user.token}/>
            ):(<Navigate to="/" replace />)
          } />

          <Route path="/livros" element={
            user && user.token && user.role ? (
              <Livros userToken={user.token} userRole={user.role}/>
            ):(<Navigate to="/" replace />)
          } />

          <Route path="/series" element={
            user && user.token && user.role ? (
              <Series userToken={user.token} userRole={user.role}/>
            ):(<Navigate to="/" replace />)
          } />

          <Route path="/perfil" element={
            user && user.token && user.id ? (
              <Perfil userToken={user.token} userId={user.id}/>
            ):(<Navigate to="/" replace />)
          } />

          <Route path="/admin/home" element={
            user && user.id && user.token && user.username && user.role? (
              <HomeAdmin userId={user.id} userToken={user.token} username={user.name} userRole={user.role} />
            ) : (
              <Navigate to="/admin/login" replace />
            )
          } />

          <Route path="/admin/filmes" element={
            user && user.token ? (
              <FilmesAdmin userToken={user.token}/>
            ):(<Navigate to="/admin/login" replace />)
          } />

          <Route path="/admin/series" element={
            user && user.token ? (
              <SeriesAdmin userToken={user.token}/>
            ):(<Navigate to="/admin/login" replace />)
          } />

          <Route path="/admin/livros" element={
            user && user.token ? (
              <LivrosAdmin userToken={user.token}/>
            ):(<Navigate to="/admin/login" replace />)
          } />

          <Route path="/admin/usuarios" element={
            user && user.token ? (
              <UsersAdmin userToken={user.token}/>
            ):(<Navigate to="/admin/login" replace />)
          } />                
        </Routes>
      </AuthContext.Provider>
    </BrowserRouter>
  );
}

export default App;
