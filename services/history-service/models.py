import sqlite3
from datetime import datetime

DATABASE = '/tmp/history.db'

def init_db():
    """Inicializa o banco de dados do histórico"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id TEXT UNIQUE NOT NULL,
            mode TEXT NOT NULL,
            white_player_id INTEGER,
            black_player_id INTEGER,
            winner TEXT,
            status TEXT NOT NULL,
            moves_count INTEGER DEFAULT 0,
            duration_seconds INTEGER DEFAULT 0,
            pgn TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_white_player 
        ON game_history(white_player_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_black_player 
        ON game_history(black_player_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_created_at 
        ON game_history(created_at DESC)
    ''')
    
    conn.commit()
    conn.close()
    print("✅ History database initialized!")

def get_db():
    """Retorna conexão com o banco"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def save_game_history(game_id, mode, white_player_id, black_player_id, 
                     winner, status, moves_count, duration_seconds, pgn):
    """Salva uma partida no histórico"""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO game_history 
            (game_id, mode, white_player_id, black_player_id, winner, 
             status, moves_count, duration_seconds, pgn)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (game_id, mode, white_player_id, black_player_id, winner,
              status, moves_count, duration_seconds, pgn))
        
        conn.commit()
        history_id = cursor.lastrowid
        conn.close()
        return history_id
    
    except sqlite3.IntegrityError:
        cursor.execute('''
            UPDATE game_history
            SET winner = ?, status = ?, moves_count = ?, 
                duration_seconds = ?, pgn = ?
            WHERE game_id = ?
        ''', (winner, status, moves_count, duration_seconds, pgn, game_id))
        conn.commit()
        conn.close()
        return None

def get_user_games(user_id, limit=20, offset=0):
    """Busca partidas de um usuário"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM game_history
        WHERE white_player_id = ? OR black_player_id = ?
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
    ''', (user_id, user_id, limit, offset))
    
    games = cursor.fetchall()
    conn.close()
    return games

def get_game_history(game_id):
    """Busca detalhes de uma partida"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM game_history WHERE game_id = ?', (game_id,))
    game = cursor.fetchone()
    conn.close()
    return game

def get_user_stats(user_id):
    """Calcula estatísticas de um usuário"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) as total
        FROM game_history
        WHERE white_player_id = ? OR black_player_id = ?
    ''', (user_id, user_id))
    total_games = cursor.fetchone()['total']
    
    cursor.execute('''
        SELECT COUNT(*) as wins
        FROM game_history
        WHERE (white_player_id = ? AND winner = 'white')
           OR (black_player_id = ? AND winner = 'black')
    ''', (user_id, user_id))
    wins = cursor.fetchone()['wins']
    
    cursor.execute('''
        SELECT COUNT(*) as losses
        FROM game_history
        WHERE (white_player_id = ? AND winner = 'black')
           OR (black_player_id = ? AND winner = 'white')
    ''', (user_id, user_id))
    losses = cursor.fetchone()['losses']
    
    draws = total_games - wins - losses
    win_rate = (wins / total_games * 100) if total_games > 0 else 0
    
    cursor.execute('''
        SELECT COUNT(*) as ai_games
        FROM game_history
        WHERE (white_player_id = ? OR black_player_id = ?)
          AND mode = 'ai'
    ''', (user_id, user_id))
    ai_games = cursor.fetchone()['ai_games']
    
    cursor.execute('''
        SELECT AVG(moves_count) as avg_moves
        FROM game_history
        WHERE white_player_id = ? OR black_player_id = ?
    ''', (user_id, user_id))
    avg_moves = cursor.fetchone()['avg_moves'] or 0
    
    cursor.execute('''
        SELECT SUM(duration_seconds) as total_time
        FROM game_history
        WHERE white_player_id = ? OR black_player_id = ?
    ''', (user_id, user_id))
    total_time = cursor.fetchone()['total_time'] or 0
    
    conn.close()
    
    return {
        'total_games': total_games,
        'wins': wins,
        'losses': losses,
        'draws': draws,
        'win_rate': round(win_rate, 2),
        'ai_games': ai_games,
        'avg_moves_per_game': round(avg_moves, 1),
        'total_time_minutes': round(total_time / 60, 1)
    }

def get_recent_games(limit=50):
    """Retorna jogos recentes"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM game_history
        ORDER BY created_at DESC
        LIMIT ?
    ''', (limit,))
    
    games = cursor.fetchall()
    conn.close()
    return games