import chess
import random
from framework.interfaces.i_chess_engine import IChessEngine

# Componente concreto de motor de xadrez que realiza movimentos aleatórios
# ESTA É UMA IMPLEMENTAÇÃO DE HOTSPOT: Fornece uma IA básica e simples ao framework
class CRandomEngine(IChessEngine):

    def __init__(self):
        # Inicializa o nome do motor
        self.name = "Random Engine"

    # Implementa a lógica para obter um movimento aleatório
    # Ignora o parâmetro difficulty completamente
    def get_best_move(self, fen: str, difficulty: str) -> str:
        # Cria o board a partir do FEN
        board = chess.Board(fen)
        
        # Obtém a lista de movimentos legais
        moves = list(board.legal_moves)
        
        # Se não houver movimentos, retorna None
        if not moves:
            return None
            
        # Retorna um movimento aleatório no formato UCI
        return random.choice(moves).uci()

    # Retorna o nome do motor
    def get_engine_name(self) -> str:
        return self.name

    # Este motor está sempre disponível pois não possui dependências externas
    def is_available(self) -> bool:
        return True
