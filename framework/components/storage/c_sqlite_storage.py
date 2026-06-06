import sqlite3
import os
from framework.interfaces.i_storage_strategy import IStorageStrategy

# Componente concreto de estratégia de armazenamento: SQLite
# ESTA É UMA IMPLEMENTAÇÃO DE HOTSPOT: Fornece persistência em banco de dados relacional
class CSQLiteStorage(IStorageStrategy):

    def __init__(self):
        self.name = "SQLite"
        self.db_path = "framework_games.db"
        self._init_db()

    # Inicializa o banco de dados e cria a tabela se necessário
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                game_id TEXT PRIMARY KEY,
                player_id INTEGER,
                mode TEXT,
                engine TEXT,
                theme TEXT,
                winner TEXT,
                moves_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    # Salva os dados de uma partida no banco
    def save_game(self, game_data: dict) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO games (game_id, player_id, mode, engine, theme, winner, moves_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                game_data["game_id"],
                game_data["player_id"],
                game_data["mode"],
                game_data["engine"],
                game_data["theme"],
                game_data["winner"],
                game_data["moves_count"]
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao salvar no SQLite: {e}")
            return False

    # Recupera uma partida específica pelo ID
    def get_game(self, game_id: str) -> dict:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM games WHERE game_id = ?', (game_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None

    # Recupera o histórico de partidas de um jogador
    def get_player_history(self, player_id: int) -> list:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM games WHERE player_id = ? ORDER BY created_at DESC', (player_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # Retorna o nome da estratégia de armazenamento
    def get_storage_name(self) -> str:
        return self.name
