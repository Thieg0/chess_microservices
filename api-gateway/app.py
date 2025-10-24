from flask import Flask
from flask_cors import CORS
import gateway

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

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
    print("🚀 Starting API Gateway on port 8000...")
    app.run(host='0.0.0.0', port=8000, debug=True)