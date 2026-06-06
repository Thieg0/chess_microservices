from framework.interfaces.i_chess_engine import IChessEngine
import chess
import random

# Implementação de HOTSPOT: Engine de IA simples usando algoritmo Minimax
class CMinimaxEngine(IChessEngine):

    def __init__(self):
        self.name = "Minimax Engine"
        # Profundidade configurada para cada nível de dificuldade
        self.depth_config = {
            "easy": 1,
            "medium": 2,
            "hard": 3
        }
        # Valores das peças para avaliação do tabuleiro
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

    def get_engine_name(self) -> str:
        """Retorna o nome do motor de xadrez"""
        return self.name

    def is_available(self) -> bool:
        """Esta engine baseada em Python está sempre disponível"""
        return True

    def _evaluate_board(self, board: chess.Board) -> int:
        """
        Avalia a posição atual do tabuleiro.
        Soma o valor das peças brancas e subtrai o das pretas.
        """
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.piece_values.get(piece.piece_type, 0)
                if piece.color == chess.WHITE:
                    score += value
                else:
                    score -= value
        return score

    def _minimax(self, board: chess.Board, depth: int, maximizing: bool) -> int:
        """
        Algoritmo Minimax simples para busca da melhor jogada.
        """
        # Caso base: profundidade zero ou fim de jogo
        if depth == 0 or board.is_game_over():
            return self._evaluate_board(board)

        if maximizing:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self._minimax(board, depth - 1, False)
                board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self._minimax(board, depth - 1, True)
                board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    def get_best_move(self, fen: str, difficulty: str) -> str:
        """
        Determina o melhor movimento usando Minimax.
        Escolhe aleatoriamente entre os movimentos com o mesmo melhor score.
        """
        board = chess.Board(fen)
        depth = self.depth_config.get(difficulty.lower(), 1)
        
        best_moves = []
        is_white = board.turn == chess.WHITE
        
        if is_white:
            best_score = float('-inf')
        else:
            best_score = float('inf')

        for move in board.legal_moves:
            board.push(move)
            # A próxima camada do minimax será do oponente
            score = self._minimax(board, depth - 1, not is_white)
            board.pop()

            if is_white:
                if score > best_score:
                    best_score = score
                    best_moves = [move.uci()]
                elif score == best_score:
                    best_moves.append(move.uci())
            else:
                if score < best_score:
                    best_score = score
                    best_moves = [move.uci()]
                elif score == best_score:
                    best_moves.append(move.uci())

        # Retorna um movimento aleatório entre os melhores encontrados
        return random.choice(best_moves) if best_moves else None
