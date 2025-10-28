import chess
import chess.engine
import random
import os
from pathlib import Path

# Configurações de dificuldade
DIFFICULTY_SETTINGS = {
    'easy': {
        'depth': 5,
        'skill_level': 5,
        'time_limit': 0.1
    },
    'medium': {
        'depth': 10,
        'skill_level': 10,
        'time_limit': 0.5
    },
    'hard': {
        'depth': 15,
        'skill_level': 20,
        'time_limit': 1.0
    }
}

# Possíveis caminhos do Stockfish
STOCKFISH_PATHS = [
    '/usr/games/stockfish',
    '/usr/local/bin/stockfish',
    '/opt/homebrew/bin/stockfish',
    'stockfish',
    '/app/stockfish',
]

def find_stockfish():
    """Procura pelo executável do Stockfish"""
    for path in STOCKFISH_PATHS:
        if Path(path).exists():
            return path
    
    import shutil
    stockfish_path = shutil.which('stockfish')
    if stockfish_path:
        return stockfish_path
    
    return None

_engine = None
_engine_path = None

def get_engine():
    """Retorna instância do Stockfish (singleton)"""
    global _engine, _engine_path
    
    if _engine is not None:
        return _engine
    
    if _engine_path is None:
        _engine_path = find_stockfish()
    
    if _engine_path is None:
        return None
    
    try:
        _engine = chess.engine.SimpleEngine.popen_uci(_engine_path)
        print(f"✅ Stockfish loaded from: {_engine_path}")
        return _engine
    except Exception as e:
        print(f"❌ Error loading Stockfish: {e}")
        return None

def is_stockfish_available():
    """Verifica se o Stockfish está disponível"""
    return get_engine() is not None

def get_best_move(fen, difficulty='medium'):
    """
    Calcula o melhor movimento usando Stockfish
    """
    try:
        board = chess.Board(fen)
        
        if board.is_game_over():
            return None
        
        engine = get_engine()
        
        if engine is None:
            return _get_random_move(board)
        
        settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS['medium'])
        
        engine.configure({"Skill Level": settings['skill_level']})
        
        result = engine.play(
            board,
            chess.engine.Limit(
                time=settings['time_limit'],
                depth=settings['depth']
            )
        )
        
        return result.move.uci()
    
    except Exception as e:
        print(f"Error calculating move: {e}")
        try:
            board = chess.Board(fen)
            return _get_random_move(board)
        except:
            return None

def _get_random_move(board):
    """Fallback: retorna um movimento aleatório legal"""
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
    return random.choice(legal_moves).uci()

def get_move_details(fen, move_uci):
    """
    Obtém detalhes sobre um movimento
    """
    try:
        board = chess.Board(fen)
        move = chess.Move.from_uci(move_uci)
        
        piece = board.piece_at(move.from_square)
        san = board.san(move)
        
        return {
            'uci': move_uci,
            'san': san,
            'piece': piece.symbol() if piece else None,
            'from': chess.square_name(move.from_square),
            'to': chess.square_name(move.to_square)
        }
    except Exception as e:
        print(f"Error getting move details: {e}")
        return {
            'uci': move_uci,
            'san': move_uci,
            'piece': None
        }

def cleanup():
    """Fecha a engine do Stockfish"""
    global _engine
    if _engine is not None:
        _engine.quit()
        _engine = None
        print("🔴 Stockfish engine closed")