from flask import Flask, request
from flask_cors import CORS
import gateway
import os

app = Flask(__name__)

# Lista de origens permitidas
ALLOWED_ORIGINS = [
    "https://chess-microservices.vercel.app",
    "http://localhost:3000",
]

def is_allowed_origin(origin):
    # Permite qualquer subdomínio do vercel.app
    # para suportar preview deployments
    if not origin:
        return False
    if origin in ALLOWED_ORIGINS:
        return True
    if origin.endswith(".vercel.app"):
        return True
    return False

CORS(app, origins=is_allowed_origin,
     supports_credentials=True)

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar se o Gateway está funcionando"""
    return {'status': 'API Gateway is running!'}, 200

# Rota catch-all que captura TODAS as requisições e delega para o gateway
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def catch_all(path):
    """Captura todas as rotas e delega para o gateway"""
    return gateway.handle_request()

# Rota raiz
@app.route('/', methods=['GET'])
def root():
    return {
        'message': 'Chess Microservices API Gateway',
        'version': '1.0.0',
        'services': {
            'auth': '/auth/*',
            'game': '/games/*',
            'ai': '/ai/*',
            'history': '/history/*'
        }
    }, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Starting API Gateway on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False) # debug=False para produção
