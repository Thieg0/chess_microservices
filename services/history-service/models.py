import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
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
    """Inicializa o banco de dados e cria as tabelas e indices"""
    conn = get_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        
        # Tabela de historico de partidas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_history (
                id SERIAL PRIMARY KEY,
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
        
        # Indices para otimizacao de consultas
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_white_player ON game_history(white_player_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_black_player ON game_history(black_player_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON game_history(created_at DESC)')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Banco de dados de historico inicializado com sucesso")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        if conn:
            conn.rollback()
            conn.close()

def save_game_history(game_id, mode, white_player_id, black_player_id, 
                     winner, status, moves_count, duration_seconds, pgn):
    """Salva ou atualiza uma partida no historico"""
    conn = get_db()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor()
        
        # Tenta inserir, se ja existir o game_id (conflito), atualiza os dados
        cursor.execute('''
            INSERT INTO game_history 
            (game_id, mode, white_player_id, black_player_id, winner, 
             status, moves_count, duration_seconds, pgn)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (game_id) DO UPDATE SET
                winner = EXCLUDED.winner,
                status = EXCLUDED.status,
                moves_count = EXCLUDED.moves_count,
                duration_seconds = EXCLUDED.duration_seconds,
                pgn = EXCLUDED.pgn
            RETURNING id
        ''', (game_id, mode, white_player_id, black_player_id, winner,
              status, moves_count, duration_seconds, pgn))
        
        result = cursor.fetchone()
        history_id = result[0] if result else None
        
        conn.commit()
        cursor.close()
        conn.close()
        return history_id
    
    except Exception as e:
        print(f"Erro ao salvar historico: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return None

def get_user_games(user_id, limit=20, offset=0):
    """Busca a lista de partidas de um usuario especifico"""
    conn = get_db()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''
            SELECT * FROM game_history
            WHERE white_player_id = %s OR black_player_id = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        ''', (user_id, user_id, limit, offset))
        
        games = cursor.fetchall()
        cursor.close()
        conn.close()
        return games
    except Exception as e:
        print(f"Erro ao buscar partidas do usuario: {e}")
        if conn:
            conn.close()
        return []

def get_game_history(game_id):
    """Busca os detalhes de uma partida pelo ID do jogo"""
    conn = get_db()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM game_history WHERE game_id = %s', (game_id,))
        game = cursor.fetchone()
        cursor.close()
        conn.close()
        return game
    except Exception as e:
        print(f"Erro ao buscar detalhes da partida: {e}")
        if conn:
            conn.close()
        return None

def get_user_stats(user_id):
    """Calcula e retorna as estatisticas consolidadas de um usuario"""
    conn = get_db()
    if not conn:
        return {}
        
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Total de partidas
        cursor.execute('''
            SELECT COUNT(*) as total
            FROM game_history
            WHERE white_player_id = %s OR black_player_id = %s
        ''', (user_id, user_id))
        total_games = cursor.fetchone()['total']
        
        if total_games == 0:
            conn.close()
            return {
                'total_games': 0, 'wins': 0, 'losses': 0, 'draws': 0,
                'win_rate': 0.0, 'ai_games': 0, 'avg_moves_per_game': 0.0,
                'total_time_minutes': 0.0
            }

        # Vitorias
        cursor.execute('''
            SELECT COUNT(*) as wins
            FROM game_history
            WHERE (white_player_id = %s AND winner = 'white')
               OR (black_player_id = %s AND winner = 'black')
        ''', (user_id, user_id))
        wins = cursor.fetchone()['wins']
        
        # Derrotas
        cursor.execute('''
            SELECT COUNT(*) as losses
            FROM game_history
            WHERE (white_player_id = %s AND winner = 'black')
               OR (black_player_id = %s AND winner = 'white')
        ''', (user_id, user_id))
        losses = cursor.fetchone()['losses']
        
        # Empates (calculado)
        draws = total_games - wins - losses
        win_rate = (wins / total_games * 100)
        
        # Jogos contra IA
        cursor.execute('''
            SELECT COUNT(*) as ai_games
            FROM game_history
            WHERE (white_player_id = %s OR black_player_id = %s)
              AND mode = 'ai'
        ''', (user_id, user_id))
        ai_games = cursor.fetchone()['ai_games']
        
        # Media de movimentos
        cursor.execute('''
            SELECT AVG(moves_count) as avg_moves
            FROM game_history
            WHERE white_player_id = %s OR black_player_id = %s
        ''', (user_id, user_id))
        avg_moves = cursor.fetchone()['avg_moves'] or 0
        
        # Tempo total de jogo
        cursor.execute('''
            SELECT SUM(duration_seconds) as total_time
            FROM game_history
            WHERE white_player_id = %s OR black_player_id = %s
        ''', (user_id, user_id))
        total_time = cursor.fetchone()['total_time'] or 0
        
        cursor.close()
        conn.close()
        
        return {
            'total_games': total_games,
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': round(win_rate, 2),
            'ai_games': ai_games,
            'avg_moves_per_game': round(float(avg_moves), 1),
            'total_time_minutes': round(float(total_time) / 60, 1)
        }
    except Exception as e:
        print(f"Erro ao calcular estatisticas: {e}")
        if conn:
            conn.close()
        return {}

def get_recent_games(limit=50):
    """Retorna os jogos mais recentes registrados no sistema"""
    conn = get_db()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('''
            SELECT * FROM game_history
            ORDER BY created_at DESC
            LIMIT %s
        ''', (limit,))
        
        games = cursor.fetchall()
        cursor.close()
        conn.close()
        return games
    except Exception as e:
        print(f"Erro ao buscar jogos recentes: {e}")
        if conn:
            conn.close()
        return []
