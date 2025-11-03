import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import os

SECRET_KEY = os.environ.get("SECRET_KEY", "TESTE_TESTE")

def generate_token(user_id):
    """Gera um token JWT para o usuário"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Expira em 24h
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """Verifica se o token é válido"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido

def token_required(f):
    """Decorator para proteger rotas que precisam de autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Pega o token do header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer TOKEN
            except IndexError:
                return jsonify({'error': 'Token format invalid'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Adiciona o user_id nos kwargs da função
        return f(payload['user_id'], *args, **kwargs)
    
    return decorated