import React, { useState, useImperativeHandle, forwardRef } from "react";
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";

const ChessBoard = forwardRef(({ boardOrientation }, ref) => {
  const [game, setGame] = useState(new Chess());

  function safeGameMutate(modify) {
    setGame((g) => {
      const updated = new Chess(g.fen());
      modify(updated);
      return updated;
    });
  }

  function onDrop(sourceSquare, targetSquare) {
    let moveMade = null;

    safeGameMutate((g) => {
      const move = g.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: "q", // promove a rainha automaticamente
      });
      if (move) moveMade = move;
    });

    // Se o movimento for inválido, o react-chessboard cancela
    return moveMade !== null;
  }

  // Função de desfazer jogada
  useImperativeHandle(ref, () => ({
    undoMove: () => {
      safeGameMutate((g) => g.undo());
    },
  }));

  return (
    <div style={{ maxWidth: "500px", margin: "0 auto" }}>
      <Chessboard
        position={game.fen()}
        onPieceDrop={onDrop}
        boardOrientation={boardOrientation}
        arePiecesDraggable={true}
        animationDuration={150}
      />
    </div>
  );
});

export default ChessBoard;
