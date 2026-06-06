import chess
import chess.engine
import shutil
import random
import os
from framework.interfaces.i_chess_engine import IChessEngine

# Componente concreto de motor de xadrez usando Stockfish
# ESTA É UMA IMPLEMENTAÇÃO DE HOTSPOT: Fornece inteligência artificial ao framework
class CStockfishEngine(IChessEngine):

    def __init__(self):
        self.name = "Stockfish Engine"
        self._engine_path = self._find_stockfish()

    # Busca o executável do Stockfish no sistema
    def _find_stockfish(self) -> str or None:
        paths = ['/usr/games/stockfish', '/usr/local/bin/stockfish', 'stockfish']
        for path in paths:
            if shutil.which(path):
                return shutil.which(path)
        return None

    # Implementa a lógica para obter a melhor jogada
    # HOTSPOT: Define como a IA deve se comportar em cada dificuldade
    def get_best_move(self, fen: str, difficulty: str) -> str:
        if not self.is_available():
            # Fallback: Se o Stockfish não estiver disponível, faz um movimento aleatório
            board = chess.Board(fen)
            moves = list(board.legal_moves)
            if not moves:
                return None
            return random.choice(moves).uci()

        # Configurações de dificuldade
        configs = {
            "easy":   {"depth": 5,  "skill_level": 5,  "time": 0.1},
            "medium": {"depth": 10, "skill_level": 10, "time": 0.5},
            "hard":   {"depth": 15, "skill_level": 20, "time": 1.0}
        }
        
        config = configs.get(difficulty, configs["medium"])

        try:
            # Inicia o motor, calcula o movimento e encerra
            with chess.engine.SimpleEngine.popen_uci(self._engine_path) as engine:
                engine.configure({"Skill Level": config["skill_level"]})
                result = engine.play(chess.Board(fen), chess.engine.Limit(time=config["time"], depth=config["depth"]))
                return result.move.uci()
        except Exception as e:
            print(f"Erro ao usar Stockfish: {e}")
            # Fallback em caso de erro técnico
            board = chess.Board(fen)
            return random.choice(list(board.legal_moves)).uci()

    # Retorna o nome amigável do motor
    def get_engine_name(self) -> str:
        return self.name

    # Verifica se o executável do Stockfish foi encontrado
    def is_available(self) -> bool:
        return self._engine_path is not None
