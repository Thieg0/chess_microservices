from flask import Flask, request, jsonify
from flask_cors import CORS
import gateway
import os

app = Flask(__name__)

# CORS simples com lista de origens permitidas
CORS(app, origins=[
    "https://chess-microservices.vercel.app",
    "http://localhost:3000"
])

# Handler para adicionar CORS em todas as respostas
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin', '')
    # Permite qualquer origem vercel.app
    if origin.endswith('.vercel.app') or origin == 'http://localhost:3000':
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

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
