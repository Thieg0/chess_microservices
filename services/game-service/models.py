import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json
import os

# URL de conexao do banco de dados PostgreSQL (Neon)
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    """Retorna uma conexao com o banco de dados PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        return None

def init_db():
    """Inicializa as tabelas do banco de dados se nao existirem"""
    conn = get_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        
        # Tabela de partidas
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
        
        # Tabela de movimentos (usando SERIAL para autoincremento)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS moves (
                id SERIAL PRIMARY KEY,
                game_id TEXT NOT NULL,
                from_square TEXT NOT NULL,
                to_square TEXT NOT NULL,
                piece TEXT NOT NULL,
                captured_piece TEXT,
                promotion TEXT,
                notation TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Banco de dados de jogos inicializado com sucesso")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        if conn:
            conn.rollback()
            conn.close()

def create_game(game_id, mode, white_player_id, black_player_id, board_state):
    """Cria uma nova partida no banco de dados"""
    conn = get_db()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO games (id, mode, white_player_id, black_player_id, 
                              board_state, current_turn, status, move_history)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (game_id, mode, white_player_id, black_player_id, 
              board_state, 'white', 'active', '[]'))
        
        conn.commit()
        cursor.close()
        conn.close()
        return game_id
    except Exception as e:
        print(f"Erro ao criar partida: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None

def get_game(game_id):
    """Busca uma partida pelo ID e retorna como dicionario"""
    conn = get_db()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM games WHERE id = %s', (game_id,))
        game = cursor.fetchone()
        cursor.close()
        conn.close()
        return game
    except Exception as e:
        print(f"Erro ao buscar partida: {e}")
        if conn:
            conn.close()
        return None

def update_game(game_id, board_state, current_turn, status, winner=None):
    """Atualiza o estado atual da partida"""
    conn = get_db()
    if not conn:
        return
        
    try:
        cursor = conn.cursor()
        if status in ['checkmate', 'stalemate', 'draw', 'resigned']:
            cursor.execute('''
                UPDATE games 
                SET board_state = %s, current_turn = %s, status = %s, 
                    winner = %s, finished_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (board_state, current_turn, status, winner, game_id))
        else:
            cursor.execute('''
                UPDATE games 
                SET board_state = %s, current_turn = %s, status = %s
                WHERE id = %s
            ''', (board_state, current_turn, status, game_id))
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao atualizar partida: {e}")
        if conn:
            conn.rollback()
            conn.close()

def add_move(game_id, from_square, to_square, piece, captured_piece, promotion, notation):
    """Adiciona um novo movimento ao historico da partida"""
    conn = get_db()
    if not conn:
        return
        
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO moves (game_id, from_square, to_square, piece, 
                              captured_piece, promotion, notation)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (game_id, from_square, to_square, piece, captured_piece, promotion, notation))
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao adicionar movimento: {e}")
        if conn:
            conn.rollback()
            conn.close()

def get_game_moves(game_id):
    """Retorna a lista de movimentos de uma partida especifica"""
    conn = get_db()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''
            SELECT * FROM moves 
            WHERE game_id = %s 
            ORDER BY timestamp ASC
        ''', (game_id,))
        moves = cursor.fetchall()
        cursor.close()
        conn.close()
        return moves
    except Exception as e:
        print(f"Erro ao buscar movimentos: {e}")
        if conn:
            conn.close()
        return []
