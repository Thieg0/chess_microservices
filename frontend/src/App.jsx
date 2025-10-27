import React, { useRef, useState } from "react";
import ChessBoard from "./ChessBoard";
import { login, register } from "./services/api";
import "./App.css";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [playerName, setPlayerName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userId, setUserId] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  
  const [boardOrientation, setBoardOrientation] = useState("white");
  const [gameKey, setGameKey] = useState(0);
  const boardRef = useRef(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await login(email, password);
      
      // Salvar token e dados do usuário
      localStorage.setItem('token', data.token);
      localStorage.setItem('userId', data.user_id);
      localStorage.setItem('userName', data.name);
      
      setUserId(data.user_id);
      setPlayerName(data.name);
      setLoggedIn(true);
    } catch (err) {
      setError(err.error || "Erro ao fazer login");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await register(playerName, email, password);
      
      // Salvar token e dados do usuário
      localStorage.setItem('token', data.token);
      localStorage.setItem('userId', data.user_id);
      localStorage.setItem('userName', playerName);
      
      setUserId(data.user_id);
      setLoggedIn(true);
    } catch (err) {
      setError(err.error || "Erro ao registrar");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('userName');
    setLoggedIn(false);
    setPlayerName("");
    setEmail("");
    setPassword("");
    setUserId(null);
  };

  const handleNewGame = () => {
    setGameKey((prev) => prev + 1);
  };

  const handleFlipBoard = () => {
    setBoardOrientation((prev) => (prev === "white" ? "black" : "white"));
  };

  const handleUndoMove = () => {
    if (boardRef.current) {
      boardRef.current.undoMove();
    }
  };

  // --- Tela de login/registro ---
  if (!loggedIn) {
    return (
      <div className="login-screen">
        <h1>♟️ Bem-vindo ao Xadrez Online</h1>
        
        {error && <div style={{color: 'red', marginBottom: '10px'}}>{error}</div>}
        
        {!showRegister ? (
          // FORMULÁRIO DE LOGIN
          <form onSubmit={handleLogin} className="login-form">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? "Entrando..." : "Entrar"}
            </button>
            <button 
              type="button" 
              onClick={() => setShowRegister(true)}
              style={{backgroundColor: '#666'}}
            >
              Criar Conta
            </button>
          </form>
        ) : (
          // FORMULÁRIO DE REGISTRO
          <form onSubmit={handleRegister} className="login-form">
            <input
              type="text"
              placeholder="Nome"
              value={playerName}
              onChange={(e) => setPlayerName(e.target.value)}
              required
            />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Senha (mínimo 6 caracteres)"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
            />
            <button type="submit" disabled={loading}>
              {loading ? "Criando..." : "Registrar"}
            </button>
            <button 
              type="button" 
              onClick={() => setShowRegister(false)}
              style={{backgroundColor: '#666'}}
            >
              Voltar ao Login
            </button>
          </form>
        )}
      </div>
    );
  }

  // --- Tela principal ---
  return (
    <div className="app-container">
      <h1 className="title">♟️ Jogo de Xadrez — {playerName}</h1>

      <div className="content">
        <div className="board-section">
          <ChessBoard
            key={gameKey}
            ref={boardRef}
            boardOrientation={boardOrientation}
            userId={userId}
          />
        </div>

        <div className="menu-section">
          <h2>Menu</h2>
          <button onClick={handleNewGame}>Novo Jogo</button>
          <button onClick={handleUndoMove}>Desfazer Jogada</button>
          <button onClick={handleFlipBoard}>Mudar Cor das Peças</button>
          <button onClick={handleLogout} style={{marginTop: '20px', backgroundColor: '#c44'}}>
            Sair
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;