import sqlite3
from datetime import datetime
import json

DATABASE = 'database.db'

def init_db():
    """Inicializa o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id TEXT PRIMARY KEY,
            mode TEXT NOT NULL,
            white_player_id INTEGER,
            black_player_id INTEGER,
            board_state TEXT NOT NULL,
            current_turn TEXT NOT NULL,
            status TEXT NOT NULL,
            winner TEXT,
            move_history TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            finished_at TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS moves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id TEXT NOT NULL,
            from_square TEXT NOT NULL,
            to_square TEXT NOT NULL,
            piece TEXT NOT NULL,
            captured_piece TEXT,
            promotion TEXT,
            notation TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Game database initialized!")

def get_db():
    """Retorna conexão com o banco"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_game(game_id, mode, white_player_id, black_player_id, board_state):
    """Cria uma nova partida"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO games (id, mode, white_player_id, black_player_id, 
                          board_state, current_turn, status, move_history)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (game_id, mode, white_player_id, black_player_id, 
          board_state, 'white', 'active', '[]'))
    
    conn.commit()
    conn.close()
    return game_id

def get_game(game_id):
    """Busca uma partida por ID"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM games WHERE id = ?', (game_id,))
    game = cursor.fetchone()
    conn.close()
    return game

def update_game(game_id, board_state, current_turn, status, winner=None):
    """Atualiza o estado de uma partida"""
    conn = get_db()
    cursor = conn.cursor()
    
    if status in ['checkmate', 'stalemate', 'draw', 'resigned']:
        cursor.execute('''
            UPDATE games 
            SET board_state = ?, current_turn = ?, status = ?, 
                winner = ?, finished_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (board_state, current_turn, status, winner, game_id))
    else:
        cursor.execute('''
            UPDATE games 
            SET board_state = ?, current_turn = ?, status = ?
            WHERE id = ?
        ''', (board_state, current_turn, status, game_id))
    
    conn.commit()
    conn.close()

def add_move(game_id, from_square, to_square, piece, captured_piece, promotion, notation):
    """Adiciona um movimento ao histórico"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO moves (game_id, from_square, to_square, piece, 
                          captured_piece, promotion, notation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (game_id, from_square, to_square, piece, captured_piece, promotion, notation))
    
    conn.commit()
    conn.close()

def get_game_moves(game_id):
    """Retorna todos os movimentos de uma partida"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM moves 
        WHERE game_id = ? 
        ORDER BY timestamp ASC
    ''', (game_id,))
    moves = cursor.fetchall()
    conn.close()
    return moves