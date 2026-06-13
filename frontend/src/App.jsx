import React, { useRef, useState, useEffect } from "react";
import ChessBoard from "./ChessBoard";
import api, { login, register } from "./services/api";
import "./App.css";

// Lê os parâmetros da URL do framework
function getFrameworkParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    theme: params.get('theme') || null,
    mode: params.get('mode') || null,
    engine: params.get('engine') || null
  };
}

function App() {
  const [servicesReady, setServicesReady] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [playerName, setPlayerName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userId, setUserId] = useState(null);
  const [gameMode, setGameMode] = useState("local");
  const [aiDifficulty, setAiDifficulty] = useState("medium");
  const [showModeSelection, setShowModeSelection] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [recommendation, setRecommendation] = useState(null);
  
  const [boardOrientation, setBoardOrientation] = useState("white");
  const [gameKey, setGameKey] = useState(0);
  const boardRef = useRef(null);

  const frameworkParams = getFrameworkParams();
  const hintsEnabled = frameworkParams.mode === 'tutorial';

  useEffect(() => {
    const wakeUpServices = async () => {
      console.log('Aquecendo serviços...');

      const services = [
        'https://chess-api-gateway-s4wz.onrender.com/health',
        'https://chess-auth-service-pzt8.onrender.com/health',
        'https://chess-game-service-mvnr.onrender.com/health',
        'https://chess-ai-service-qaen.onrender.com/health',
        'https://chess-history-service-mc3l.onrender.com/health'
      ];

      try {
        await Promise.all(
          services.map(url => 
            fetch(url).catch(err => console.log('Acordando...', url))
          )
        );
        console.log('Todos os serviços estão acordados!');
        setServicesReady(true);
      } catch (error) {
        console.log('Alguns serviços ainda estão acordando...');
        setServicesReady(true); // Mesmo que falhe, prosseguir
      }
    };

    wakeUpServices();
  }, []);

  if (!servicesReady) {
    return (
      <div style={{textAlign: 'center', marginTop: '100px'}}>
        <h2>🔥 Aquecendo serviços...</h2>
        <p>Aguarde ~30 segundos (primeira vez pode demorar)</p>
        <p>⏳ Render free tier está acordando os microserviços...</p>
      </div>
    );
  }

  const fetchRecommendation = async (userId) => {
    try {
      const response = await api.get(`/recommendations/${userId}`);
      setRecommendation(response.data);
    } catch (error) {
      console.error('Erro ao buscar recomendação:', error);
    }
  };

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
      fetchRecommendation(data.user_id);

      // Se veio do framework, inicia automaticamente
      if (frameworkParams.theme || frameworkParams.mode) {
        const mode = frameworkParams.mode === 'local' ? 'local' : 'ai';
        const difficulty = frameworkParams.engine === 'minimax' ? 'easy' : 'medium';
        setTimeout(() => startNewGame(mode, difficulty), 500);
      }
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
      fetchRecommendation(data.user_id);

      // Se veio do framework, inicia automaticamente
      if (frameworkParams.theme || frameworkParams.mode) {
        const mode = frameworkParams.mode === 'local' ? 'local' : 'ai';
        const difficulty = frameworkParams.engine === 'minimax' ? 'easy' : 'medium';
        setTimeout(() => startNewGame(mode, difficulty), 500);
      }
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
    setShowModeSelection(true);
  };

  const startNewGame = (mode, difficulty = 'medium') => {
    setGameMode(mode);
    setAiDifficulty(difficulty);
    setGameKey((prevKey) => prevKey + 1); // Forçar re-montagem do ChessBoard
    setShowModeSelection(false);
  }

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
      {/* Modal de seleção de modo */}
      {showModeSelection && (
      <div className="modal-overlay">
        <div className="modal">
          <h2>Escolha o Modo de Jogo</h2>
          
          <button onClick={() => startNewGame('local')}>
            👥 2 Jogadores Local
          </button>
          
          <div className="ai-options">
            <h3>Jogar contra IA</h3>
            <button onClick={() => startNewGame('ai', 'easy')}>
              🤖 IA Fácil
            </button>
            <button onClick={() => startNewGame('ai', 'medium')}>
              🤖 IA Médio
            </button>
            <button onClick={() => startNewGame('ai', 'hard')}>
              🤖 IA Difícil
            </button>
          </div>
          
          <button 
            onClick={() => setShowModeSelection(false)}
            style={{backgroundColor: '#999', marginTop: '20px'}}
          >
            Cancelar
          </button>
        </div>
      </div>
    )}

      {recommendation && (
        <div style={{
          textAlign: 'center',
          padding: '10px',
          margin: '10px auto',
          maxWidth: '500px',
          backgroundColor: '#e8f4f8',
          borderRadius: '8px',
          border: '1px solid #9370DB'
        }}>
          <strong>💡 Recomendação:</strong>{' '}
          {recommendation.recommended_mode === 'ai' ? '🤖 Jogue contra IA' : '👥 Jogue Local'}
          {' | '}
          Dificuldade: <strong>{recommendation.recommended_difficulty}</strong>
          {' | '}
          <small style={{color: '#666'}}>{recommendation.reason}</small>
        </div>
      )}

      <div className="content">
        <div className="board-section">
          <ChessBoard
            key={gameKey}
            ref={boardRef}
            boardOrientation={boardOrientation}
            userId={userId}
            gameMode={gameMode}
            aiDifficulty={aiDifficulty}
            hintsEnabled={hintsEnabled}
          />
        </div>

        <div className="menu-section">
          <h2>Menu</h2>
          <p>Modo: {gameMode === 'local' ? '👥 Local' : `🤖 IA (${aiDifficulty})`}</p>
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

