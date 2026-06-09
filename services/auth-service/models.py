import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
import os
import sys

# Pega a URL de conexão do PostgreSQL (Neon) das variáveis de ambiente
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db():
    """Retorna uma conexão com o banco de dados PostgreSQL"""
    try:
        # Conecta ao PostgreSQL usando a string de conexão
        # sslmode=require é geralmente necessário para o Neon
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        return conn
    except Exception as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        return None

def init_db():
    """Inicializa o banco de dados e cria as tabelas se não existirem"""
    conn = get_db()
    if not conn:
        print("Não foi possível inicializar o banco de dados.")
        return

    try:
        cursor = conn.cursor()
        # No PostgreSQL usamos SERIAL para autoincremento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash BYTEA NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Banco de dados PostgreSQL inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar tabelas: {e}")
        if conn:
            conn.rollback()
            conn.close()

def create_user(name, email, password):
    """Cria um novo usuário no banco de dados"""
    conn = get_db()
    if not conn:
        return None
        
    cursor = conn.cursor()
    # Hash da senha usando bcrypt
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        # No PostgreSQL usamos %s em vez de ? e RETURNING para pegar o ID inserido
        cursor.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id',
            (name, email, password_hash)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return user_id
    except psycopg2.IntegrityError:
        conn.rollback()
        conn.close()
        return None
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        conn.rollback()
        conn.close()
        return None
    
def get_user_by_email(email):
    """Busca um usuário pelo email usando RealDictCursor para manter compatibilidade"""
    conn = get_db()
    if not conn:
        return None
        
    try:
        # RealDictCursor permite acessar colunas pelo nome como um dicionário
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        print(f"Erro ao buscar usuário por email: {e}")
        conn.close()
        return None

def get_user_by_id(user_id):
    """Busca um usuário pelo ID"""
    conn = get_db()
    if not conn:
        return None
        
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        print(f"Erro ao buscar usuário por ID: {e}")
        conn.close()
        return None

def verify_password(stored_password_hash, password):
    """Verifica se a senha fornecida corresponde ao hash armazenado"""
    # Se o hash vier do banco como memoryview ou bytes (PostgreSQL BYTEA)
    if isinstance(stored_password_hash, memoryview):
        stored_password_hash = bytes(stored_password_hash)
    return bcrypt.checkpw(password.encode('utf-8'), stored_password_hash)
