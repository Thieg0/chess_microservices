from flask import Flask, request, jsonify
from flask_cors import CORS
import models
import auth

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

# Inicializa o banco quando o app inicia
models.init_db()

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar se o serviço está funcionando"""
    return jsonify({'status': 'Auth Service is running!'}), 200

@app.route('/auth/register', methods=['POST'])
def register():
    """Registra um novo usuário"""
    data = request.json
    
    # Validação dos dados
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Name, email and password are required'}), 400
    
    name = data['name']
    email = data['email']
    password = data['password']
    
    # Validação de senha (mínimo 6 caracteres)
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Tenta criar o usuário
    user_id = models.create_user(name, email, password)
    
    if user_id is None:
        return jsonify({'error': 'Email already exists'}), 409
    
    # Gera token JWT
    token = auth.generate_token(user_id)
    
    return jsonify({
        'message': 'User created successfully',
        'user_id': user_id,
        'token': token
    }), 201

@app.route('/auth/login', methods=['POST'])
def login():
    """Faz login de um usuário"""
    data = request.json
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    email = data['email']
    password = data['password']
    
    # Busca usuário no banco
    user = models.get_user_by_email(email)
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Verifica senha
    if not models.verify_password(user['password_hash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Gera token
    token = auth.generate_token(user['id'])
    
    return jsonify({
        'message': 'Login successful',
        'user_id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'token': token
    }), 200

@app.route('/auth/verify-token', methods=['POST'])
def verify_token_route():
    """Verifica se um token é válido (usado pelo API Gateway)"""
    data = request.json
    
    if not data or not data.get('token'):
        return jsonify({'error': 'Token is required'}), 400
    
    token = data['token']
    payload = auth.verify_token(token)
    
    if not payload:
        return jsonify({'valid': False}), 401
    
    return jsonify({
        'valid': True,
        'user_id': payload['user_id']
    }), 200

@app.route('/auth/users/<int:user_id>', methods=['GET'])
@auth.token_required
def get_user(current_user_id, user_id):
    """Busca informações de um usuário (rota protegida)"""
    user = models.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'created_at': user['created_at']
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)