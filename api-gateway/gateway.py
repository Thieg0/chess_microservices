import requests
from flask import request, jsonify
import os

# URLs dos microserviços (vêm das variáveis de ambiente)
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:8001')
GAME_SERVICE_URL = os.getenv('GAME_SERVICE_URL', 'http://localhost:8003')
AI_SERVICE_URL = os.getenv('AI_SERVICE_URL', 'http://localhost:8004')
HISTORY_SERVICE_URL = os.getenv('HISTORY_SERVICE_URL', 'http://localhost:8005')
RECOMMENDATION_SERVICE_URL = os.getenv('RECOMMENDATION_SERVICE_URL', 'http://localhost:8006')
MULTIPLAYER_SERVICE_URL = os.getenv('MULTIPLAYER_SERVICE_URL', 'http://localhost:8007')

# Rotas que não precisam de autenticação
PUBLIC_ROUTES = [
    '/auth/register',
    '/auth/login',
    '/health',
    '/rooms' # Listagem de salas é pública
]

def verify_token(token):
    """Verifica o token JWT com o serviço de autenticação."""
    try:
        response = requests.post(
            f'{AUTH_SERVICE_URL}/auth/verify-token',
            json={'token': token},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('valid', False), data.get('user_id')
        return False, None
    except Exception as e:
        print(f'Error verifying token: {e}')
        return False, None
    
def is_public_route(path):
    """Verifica se a rota é pública."""
    for public_route in PUBLIC_ROUTES:
        if path.startswith(public_route):
            return True
    return False

def get_service_url(path):
    """Determina qual microsserviço deve receber a requisição baseado no path"""
    print(f"🔍 Checking path: {path}")  # DEBUG
    
    if path.startswith('/auth'):
        print(f"✅ Routing to AUTH_SERVICE_URL: {AUTH_SERVICE_URL}")
        return AUTH_SERVICE_URL
    elif path.startswith('/games'):
        print(f"✅ Routing to GAME_SERVICE_URL: {GAME_SERVICE_URL}")
        return GAME_SERVICE_URL
    elif path.startswith('/ai'):
        print(f"✅ Routing to AI_SERVICE_URL: {AI_SERVICE_URL}")
        return AI_SERVICE_URL
    elif path.startswith('/history'):
        print(f"✅ Routing to HISTORY_SERVICE_URL: {HISTORY_SERVICE_URL}")
        return HISTORY_SERVICE_URL
    elif path.startswith('/recommendations'):
        print(f"✅ Routing to RECOMMENDATION_SERVICE_URL: {RECOMMENDATION_SERVICE_URL}")
        return RECOMMENDATION_SERVICE_URL
    elif path.startswith('/multiplayer') or path.startswith('/rooms'):
        print(f"✅ Routing to MULTIPLAYER_SERVICE_URL: {MULTIPLAYER_SERVICE_URL}")
        return MULTIPLAYER_SERVICE_URL
    else:
        print(f"❌ No service found for path: {path}")
        return None
    
def proxy_request(path, method, data=None, headers=None):
    """Faz proxy da requisição para o microserviço apropriado."""
    # Determina qual serviço usar
    service_url = get_service_url(path)

    if not service_url:
        return jsonify({'error': 'Service not found'}), 404
    
    # Monta a URL completa
    url = f'{service_url}{path}'

    # Prepara os headers (sem o authorization)
    proxy_headers = {
        'Content-Type': 'application/json'
    }

    try:
        # Faz a requisição para o microserviço
        if method == 'GET':
            response = requests.get(url, headers=proxy_headers, timeout=30)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=proxy_headers, timeout=30)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=proxy_headers, timeout=30)
        elif method == 'DELETE':
            response = requests.delete(url, headers=proxy_headers, timeout=30)
        else:
            return jsonify({'error': 'Method not allowed'}), 405
        
        # Retorna a resposta do microserviço
        try: 
            return jsonify(response.json()), response.status_code
        except:
            return jsonify({'data': response.text}), response.status_code
        
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Service timeout'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Service unavailable'}), 503
    except Exception as e:
        print(f'Error proxying request: {e}')
        return jsonify({'error': 'Internal gateway error'}), 500

def handle_request():
    """
        Handler principal que:
        1. verifica se a rota precisa de autenticação,
        2. verifica o token se necessário,
        3. faz proxy da requisição para o microserviço apropriado.
    """

    path = request.path
    method = request.method
    data = request.get_json() if request.is_json else None

    # Se não for rota pública, verifica autenticação
    if not is_public_route(path):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'error': 'Authorization header missing'}), 401
        
        # Extrai o token (formato: "Bearer TOKEN")
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        # Verifica o token
        is_valid, user_id = verify_token(token)

        if not is_valid:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Token válido, pode prosseguir
        print(f'Authenticated request from user: {user_id}')

    # Faz proxy da requisição
    return proxy_request(path, method, data, request.headers)