import chess
import uuid

class ChessGame:
    """Classe para gerenciar a lógica do jogo de xadrez"""
    
    def __init__(self, game_id=None, fen=None):
        """
        Inicializa um jogo de xadrez
        game_id: ID do jogo (gera um novo se None)
        fen: Estado do tabuleiro em notação FEN (usa posição inicial se None)
        """
        self.game_id = game_id or str(uuid.uuid4())
        self.board = chess.Board(fen) if fen else chess.Board()
    
    def get_board_state(self):
        """Retorna o estado atual do tabuleiro em FEN"""
        return self.board.fen()
    
    def get_current_turn(self):
        """Retorna de quem é o turno ('white' ou 'black')"""
        return 'white' if self.board.turn == chess.WHITE else 'black'
    
    def is_valid_move(self, from_square, to_square, promotion=None):
        """
        Verifica se um movimento é válido
        from_square: casa de origem (ex: 'e2')
        to_square: casa de destino (ex: 'e4')
        promotion: peça para promoção (ex: 'q' para rainha)
        """
        try:
            move = chess.Move.from_uci(from_square + to_square + (promotion or ''))
            return move in self.board.legal_moves
        except:
            return False
    
    def make_move(self, from_square, to_square, promotion=None):
        """
        Executa um movimento
        Retorna: dict com informações do movimento ou None se inválido
        """
        try:
            uci_move = from_square + to_square + (promotion or '')
            move = chess.Move.from_uci(uci_move)
            
            if move not in self.board.legal_moves:
                return None
            
            # Captura informações antes do movimento
            piece = self.board.piece_at(move.from_square)
            captured_piece = self.board.piece_at(move.to_square)
            
            # Executa o movimento
            san_notation = self.board.san(move)  # Notação algébrica
            self.board.push(move)
            
            return {
                'from': from_square,
                'to': to_square,
                'piece': piece.symbol() if piece else None,
                'captured': captured_piece.symbol() if captured_piece else None,
                'promotion': promotion,
                'notation': san_notation,
                'fen': self.board.fen()
            }
        except Exception as e:
            print(f"Error making move: {e}")
            return None
    
    def get_valid_moves(self, square=None):
        """
        Retorna lista de movimentos válidos
        square: se especificado, retorna apenas movimentos dessa casa
        """
        if square:
            try:
                square_index = chess.parse_square(square)
                moves = [
                    move.uci() for move in self.board.legal_moves 
                    if move.from_square == square_index
                ]
                return moves
            except:
                return []
        else:
            return [move.uci() for move in self.board.legal_moves]
    
    def is_check(self):
        """Verifica se o rei está em xeque"""
        return self.board.is_check()
    
    def is_checkmate(self):
        """Verifica se é xeque-mate"""
        return self.board.is_checkmate()
    
    def is_stalemate(self):
        """Verifica se é afogamento (empate)"""
        return self.board.is_stalemate()
    
    def is_insufficient_material(self):
        """Verifica empate por material insuficiente"""
        return self.board.is_insufficient_material()
    
    def is_game_over(self):
        """Verifica se o jogo acabou"""
        return self.board.is_game_over()
    
    def get_game_status(self):
        """
        Retorna o status do jogo
        Retorna: dict com status e vencedor (se houver)
        """
        if self.is_checkmate():
            winner = 'black' if self.board.turn == chess.WHITE else 'white'
            return {'status': 'checkmate', 'winner': winner}
        
        if self.is_stalemate():
            return {'status': 'stalemate', 'winner': None}
        
        if self.is_insufficient_material():
            return {'status': 'draw', 'winner': None}
        
        if self.is_check():
            return {'status': 'check', 'winner': None}
        
        return {'status': 'active', 'winner': None}
    
    def get_move_history(self):
        """Retorna histórico de movimentos em notação SAN"""
        return [self.board.san(move) for move in self.board.move_stack]
    
    def resign(self, color):
        """
        Um jogador desiste
        color: 'white' ou 'black'
        """
        winner = 'black' if color == 'white' else 'white'
        return {'status': 'resigned', 'winner': winner}