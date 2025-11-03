from flask import Flask, request, jsonify
from flask_cors import CORS
import models
import game_logic
import uuid
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False para produção

app = Flask(__name__)

CORS(app, origins=[
    "https://chess-microservices.vercel.app",
    "http://localhost:3000",
    "https://*.onrender.com"  # Permitir chamadas entre serviços Render
])

# Inicializa o banco quando o app inicia
models.init_db()

# Dicionário para armazenar jogos ativos em memória (cache)
active_games = {}

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar se o serviço está funcionando"""
    return jsonify({'status': 'Game Service is running!'}), 200

@app.route('/games', methods=['POST'])
def create_game():
    """
    Cria uma nova partida
    Body: {
        "mode": "local" ou "ai",
        "white_player_id": 1,
        "black_player_id": 2 (ou null se for vs IA)
    }
    """
    data = request.json
    
    if not data or not data.get('mode'):
        return jsonify({'error': 'Mode is required'}), 400
    
    mode = data['mode']
    white_player_id = data.get('white_player_id')
    black_player_id = data.get('black_player_id')
    
    if mode not in ['local', 'ai']:
        return jsonify({'error': 'Mode must be "local" or "ai"'}), 400
    
    # Cria o jogo
    game_id = str(uuid.uuid4())
    chess_game = game_logic.ChessGame(game_id)
    
    # Salva no banco
    models.create_game(
        game_id, 
        mode, 
        white_player_id, 
        black_player_id,
        chess_game.get_board_state()
    )
    
    # Salva em memória para acesso rápido
    active_games[game_id] = chess_game
    
    return jsonify({
        'game_id': game_id,
        'mode': mode,
        'board_state': chess_game.get_board_state(),
        'current_turn': chess_game.get_current_turn(),
        'status': 'active'
    }), 201

@app.route('/games/<game_id>', methods=['GET'])
def get_game(game_id):
    """Retorna o estado atual de uma partida"""
    
    # Tenta pegar do cache
    if game_id in active_games:
        chess_game = active_games[game_id]
    else:
        # Busca no banco
        game = models.get_game(game_id)
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        # Recria o jogo a partir do FEN
        chess_game = game_logic.ChessGame(game_id, game['board_state'])
        active_games[game_id] = chess_game
    
    game_status = chess_game.get_game_status()
    
    return jsonify({
        'game_id': game_id,
        'board_state': chess_game.get_board_state(),
        'current_turn': chess_game.get_current_turn(),
        'status': game_status['status'],
        'winner': game_status.get('winner'),
        'is_check': chess_game.is_check(),
        'is_game_over': chess_game.is_game_over()
    }), 200

@app.route('/games/<game_id>/move', methods=['POST'])
def make_move(game_id):
    """
    Executa um movimento
    Body: {
        "from": "e2",
        "to": "e4",
        "promotion": "q" (opcional, para promoção de peão)
    }
    """
    data = request.json

    print(f"🎯 Recebido movimento: {data}")  # ADICIONE
    print(f"🎲 Game ID: {game_id}")  # ADICIONE
    
    if not data or not data.get('from') or not data.get('to'):
        return jsonify({'error': 'from and to squares are required'}), 400
    
    from_square = data['from']
    to_square = data['to']
    promotion = data.get('promotion')

    print(f"📍 From: {from_square}, To: {to_square}, Promotion: {promotion}")  # ADICIONE
    
    # Busca o jogo
    if game_id not in active_games:
        game = models.get_game(game_id)
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        chess_game = game_logic.ChessGame(game_id, game['board_state'])
        active_games[game_id] = chess_game
    else:
        chess_game = active_games[game_id]
    
    # Verifica se o jogo já acabou
    if chess_game.is_game_over():
        return jsonify({'error': 'Game is already over'}), 400
    
    # Tenta fazer o movimento
    move_result = chess_game.make_move(from_square, to_square, promotion)
    
    if not move_result:
        return jsonify({'error': 'Invalid move'}), 400
    
    # Salva o movimento no banco
    models.add_move(
        game_id,
        from_square,
        to_square,
        move_result['piece'],
        move_result['captured'],
        move_result['promotion'],
        move_result['notation']
    )
    
    # Verifica status do jogo
    game_status = chess_game.get_game_status()
    
    # Atualiza no banco
    models.update_game(
        game_id,
        chess_game.get_board_state(),
        chess_game.get_current_turn(),
        game_status['status'],
        game_status.get('winner')
    )
    
    return jsonify({
        'success': True,
        'move': move_result,
        'board_state': chess_game.get_board_state(),
        'current_turn': chess_game.get_current_turn(),
        'status': game_status['status'],
        'winner': game_status.get('winner'),
        'is_check': chess_game.is_check(),
        'is_checkmate': chess_game.is_checkmate(),
        'is_game_over': chess_game.is_game_over()
    }), 200

@app.route('/games/<game_id>/valid-moves', methods=['GET'])
def get_valid_moves(game_id):
    """
    Retorna movimentos válidos
    Query param: ?square=e2 (opcional, para movimentos de uma casa específica)
    """
    square = request.args.get('square')
    
    # Busca o jogo
    if game_id not in active_games:
        game = models.get_game(game_id)
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        chess_game = game_logic.ChessGame(game_id, game['board_state'])
        active_games[game_id] = chess_game
    else:
        chess_game = active_games[game_id]
    
    valid_moves = chess_game.get_valid_moves(square)
    
    return jsonify({
        'valid_moves': valid_moves,
        'count': len(valid_moves)
    }), 200

@app.route('/games/<game_id>/resign', methods=['POST'])
def resign_game(game_id):
    """
    Jogador desiste
    Body: {
        "color": "white" ou "black"
    }
    """
    data = request.json
    
    if not data or not data.get('color'):
        return jsonify({'error': 'color is required'}), 400
    
    color = data['color']
    
    if color not in ['white', 'black']:
        return jsonify({'error': 'color must be "white" or "black"'}), 400
    
    # Busca o jogo
    if game_id not in active_games:
        game = models.get_game(game_id)
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        chess_game = game_logic.ChessGame(game_id, game['board_state'])
        active_games[game_id] = chess_game
    else:
        chess_game = active_games[game_id]
    
    result = chess_game.resign(color)
    
    # Atualiza no banco
    models.update_game(
        game_id,
        chess_game.get_board_state(),
        chess_game.get_current_turn(),
        result['status'],
        result['winner']
    )
    
    return jsonify({
        'message': f'{color} resigned',
        'status': result['status'],
        'winner': result['winner']
    }), 200

@app.route('/games/<game_id>/history', methods=['GET'])
def get_move_history(game_id):
    """Retorna o histórico completo de movimentos"""
    
    game = models.get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    moves = models.get_game_moves(game_id)
    
    move_list = []
    for move in moves:
        move_list.append({
            'from': move['from_square'],
            'to': move['to_square'],
            'piece': move['piece'],
            'captured': move['captured_piece'],
            'notation': move['notation'],
            'timestamp': move['timestamp']
        })
    
    return jsonify({
        'game_id': game_id,
        'moves': move_list,
        'total_moves': len(move_list)
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003, debug=True)