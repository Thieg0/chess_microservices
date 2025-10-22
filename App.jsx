import React, { useRef, useState } from "react";
import ChessBoard from "./ChessBoard";
import "./App.css";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [playerName, setPlayerName] = useState("");
  const [boardOrientation, setBoardOrientation] = useState("white");
  const [gameKey, setGameKey] = useState(0);
  const boardRef = useRef(null);

  const handleLogin = (e) => {
    e.preventDefault();
    if (playerName.trim() !== "") {
      setLoggedIn(true);
    }
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

  // --- Tela de login ---
  if (!loggedIn) {
    return (
      <div className="login-screen">
        <h1>♟️ Bem-vindo ao Xadrez Online</h1>
        <form onSubmit={handleLogin} className="login-form">
          <input
            type="text"
            placeholder="Digite seu nome"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
          />
          <button type="submit">Entrar</button>
        </form>
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
          />
        </div>

        <div className="menu-section">
          <h2>Menu</h2>
          <button onClick={handleNewGame}>Novo Jogo</button>
          <button onClick={handleUndoMove}>Desfazer Jogada</button>
          <button onClick={handleFlipBoard}>Mudar Cor das Peças</button>
        </div>
      </div>
    </div>
  );
}

export default App;
