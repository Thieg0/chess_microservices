import sqlite3
import bcrypt
from datetime import datetime

DATABASE = "database.db"

def init_db():
    """Inicializa o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    cursor = sqlite3.connect(DATABASE)

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       email TEXT UNIQUE NOT NULL,
                       password_hash TEXT NOT NULL,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                ''')
    
def get_db():
    """Retorna uma conexão com o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(name, email, password):
    """Cria um novo usuário no banco de dados"""
    conn = get_db()
    cursor = conn.cursor()

    # Hash da senha
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                       (name, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None
    
def get_user_by_email(email):
    """Busca um usuário pelo email"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Busca um usuário pelo ID"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_password(stored_password_hash, password):
    """Verifica se a senha fornecida corresponde ao hash armazenado"""
    return bcrypt.checkpw(password.encode('utf-8'), stored_password_hash)


    