import React, { useState, useEffect, useImperativeHandle, forwardRef, useRef } from "react";
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";
import { createGame, makeMove, getAIMove, getHint } from "./services/api";

const ChessBoard = forwardRef(({ boardOrientation, userId, gameMode = 'local', aiDifficulty = 'medium', hintsEnabled = false }, ref) => {
  const [game, setGame] = useState(new Chess());
  const [gameId, setGameId] = useState(null);
  const [currentTurn, setCurrentTurn] = useState("white");
  const [gameStatus, setGameStatus] = useState("active");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [waitingForAI, setWaitingForAI] = useState(false);
  const [hint, setHint] = useState(null);
  const [loadingHint, setLoadingHint] = useState(false);
  const gameCreated = useRef(false);

  // Lê o tema passado pelo framework via URL
  const urlParams = new URLSearchParams(window.location.search);
  const frameworkTheme = urlParams.get('theme');

  // Define as cores do tabuleiro baseado no tema
  const boardColors = {
    colorful: {
      light: { backgroundColor: '#FFE4B5' },
      dark:  { backgroundColor: '#9370DB' }
    },
    classic: {
      light: { backgroundColor: '#F0D9B5' },
      dark:  { backgroundColor: '#B58863' }
    },
    modern: {
      light: { backgroundColor: '#EEEED2' },
      dark:  { backgroundColor: '#769656' }
    }
  };

  // Pega as cores do tema atual ou usa o padrão
  const currentTheme = boardColors[frameworkTheme] || boardColors.classic;

  // Criar nova partida quando o componente monta
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (userId && !gameCreated.current) {
      gameCreated.current = true;
      initializeGame();
    }
  }, [userId]);

  const initializeGame = async () => {
    setLoading(true);
    setMessage("Criando nova partida...");

    console.log("=== INIT GAME ===");
    console.log("UserId:", userId);
    console.log("GameMode:", gameMode);
    
    try {
      // Criar partida no backend usando o modo correto
      console.log("Chamando createGame...");
      const data = await createGame(gameMode, userId, userId);
      console.log("createGame retornou:", data);
      
      setGameId(data.game_id);
      setCurrentTurn(data.current_turn);
      setGameStatus(data.status);
      
      // Inicializar tabuleiro com o estado do backend
      const newGame = new Chess(data.board_state);
      setGame(newGame);
      
      setMessage("Partida criada! Seu turno.");
    } catch (error) {
      setMessage("Erro ao criar partida: " + (error.error || "Erro desconhecido"));
      console.error(error);
    } finally {
      setLoading(false);
    }
  };
  
  const makeAIMove = async () => {
    if (gameMode !== 'ai' || currentTurn !== 'black') {
      return;
    }

    setWaitingForAI(true);
    setMessage("🤖 IA está pensando...");

    try {
      const currentFen = game.fen();
    
      console.log("Solicitando movimento da IA...");
      const aiResponse = await getAIMove(currentFen, aiDifficulty);
      
      if (!aiResponse.success) {
        throw new Error("IA não retornou movimento válido");
      }

      const aiMove = aiResponse.move;
      console.log("IA sugeriu:", aiMove);

      await new Promise(resolve => setTimeout(resolve, 500));

      const data = await makeMove(
        gameId, 
        aiMove.from, 
        aiMove.to, 
        aiMove.promotion
      );

      const updatedGame = new Chess(data.board_state);
      setGame(updatedGame);
      setCurrentTurn(data.current_turn);
      setGameStatus(data.status);

      if (data.is_checkmate) {
        setMessage(`Xeque-mate! ${data.winner === 'white' ? 'Você venceu!' : 'IA venceu!'}`);
      } else if (data.is_check) {
        setMessage("Xeque! Seu turno.");
      } else {
        setMessage("Seu turno.");
      }

    } catch (error) {
      console.error("Erro na jogada da IA:", error);
      setMessage("Erro: IA não conseguiu jogar");
    } finally {
      setWaitingForAI(false);
    }
  };

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (
      gameMode === 'ai' && 
      currentTurn === 'black' && 
      gameStatus === 'active' && 
      !waitingForAI &&
      gameId
    ) {
      const timer = setTimeout(() => {
        makeAIMove();
      }, 800);

      return () => clearTimeout(timer);
    }
  }, [currentTurn, gameMode, gameStatus, waitingForAI, gameId]);

  // Busca dica de melhor movimento
  const fetchHint = async () => {
    if (!hintsEnabled || !gameId) return;
    setLoadingHint(true);
    setHint(null);
    try {
      const currentFen = game.fen();
      const response = await getHint(currentFen);
      if (response.success) {
        setHint(response.hint);
      }
    } catch (error) {
      console.error("Erro ao buscar dica:", error);
    } finally {
      setLoadingHint(false);
    }
  };
  
  
const onDrop = async (sourceSquare, targetSquare) => {
  console.log("🎯 Movimento:", sourceSquare, "->", targetSquare);
  
  if (loading || (gameStatus !== "active" && gameStatus !== "check") || waitingForAI) {
    console.log("❌ Bloqueado - loading ou jogo não ativo");
    return false;
  }

  if (gameMode === 'ai' && currentTurn === 'black') {
    setMessage("Aguarde o turno da IA");
    return false;
  }

  if (!gameId) {
    console.log("❌ Sem gameId ainda");
    return false;
  }

  // NÃO VALIDAR LOCALMENTE - enviar direto para o backend!
  setLoading(true);
  setMessage("Processando movimento...");

  try {
    console.log("📤 Enviando movimento para API...");
    const data = await makeMove(gameId, sourceSquare, targetSquare, null);
    console.log("✅ Resposta da API:", data);
    
    // Atualizar estado do jogo com resposta do backend
    const updatedGame = new Chess(data.board_state);
    setGame(updatedGame);
    setCurrentTurn(data.current_turn);
    setGameStatus(data.status);

    // Limpa a dica após o movimento
    setHint(null);

    // Mensagens baseadas no status
    if (data.is_checkmate) {
      setMessage(`Xeque-mate! ${data.winner === 'white' ? 'Brancas' : 'Pretas'} venceram!`);
    } else if (data.is_check) {
      setMessage("Xeque!");
    } else if (data.status === "stalemate") {
      setMessage("Empate por afogamento!");
    } else {
      setMessage(`Turno: ${data.current_turn === 'white' ? 'Brancas' : 'Pretas'}`);
    }

    return true;
  } catch (error) {
    console.error("❌ Erro no movimento:", error);
    setMessage("Erro: " + (error.error || "Movimento inválido"));
    
    // NÃO atualizar o tabuleiro local em caso de erro
    // O backend rejeitou, então mantém como está
    return false;
  } finally {
    setLoading(false);
  }
};

  // Função de desfazer jogada (apenas local, não no backend)
  useImperativeHandle(ref, () => ({
    undoMove: () => {
      if (game.history().length > 0) {
        const gameCopy = new Chess(game.fen());
        gameCopy.undo();
        setGame(gameCopy);
        setMessage("Jogada desfeita (apenas localmente)");
        setHint(null);
      } else {
        setMessage("Nenhuma jogada para desfazer");
      }
    },
  }));

  return (
    <div style={{ maxWidth: "500px", margin: "0 auto" }}>
      {/* Mensagem de status */}
      <div style={{
        textAlign: 'center',
        padding: '10px',
        marginBottom: '10px',
        backgroundColor: gameStatus === 'checkmate' ? '#ffcccc' : 
                         gameStatus === 'check' ? '#fff3cd' : 
                         '#e8f4f8',
        borderRadius: '5px',
        fontWeight: 'bold'
      }}>
        {message || `Turno: ${currentTurn === 'white' ? 'Brancas' : 'Pretas'}`}
      </div>

      {/* Tabuleiro */}
      <Chessboard
        position={game.fen()}
        onPieceDrop={onDrop}
        boardOrientation={boardOrientation}
        arePiecesDraggable={true}
        animationDuration={150}
        customDarkSquareStyle={currentTheme.dark}
        customLightSquareStyle={currentTheme.light}
      />

      {hintsEnabled && (
        <div style={{
          textAlign: 'center',
          marginTop: '10px'
        }}>
          <button
            onClick={fetchHint}
            disabled={loadingHint || gameStatus !== 'active'}
            style={{
              padding: '8px 16px',
              backgroundColor: '#9370DB',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '0.9rem'
            }}
          >
            {loadingHint ? '⏳ Buscando dica...' : '💡 Pedir Dica'}
          </button>
          {hint && (
            <div style={{
              marginTop: '8px',
              padding: '8px',
              backgroundColor: '#f0e6ff',
              borderRadius: '5px',
              color: '#333',
              fontSize: '0.9rem'
            }}>
              💡 Dica: Mova a peça de 
              <strong> {hint.from}</strong> para 
              <strong> {hint.to}</strong>
              {hint.san && ` (${hint.san})`}
            </div>
          )}
        </div>
      )}

      {/* Info adicional */}
      <div style={{
        textAlign: 'center',
        marginTop: '10px',
        fontSize: '0.9rem',
        color: '#666'
      }}>
        {gameId && <div>ID da Partida: {gameId.substring(0, 8)}...</div>}
        <div>Movimentos: {game.history().length}</div>
      </div>
    </div>
  );
});

export default ChessBoard;
