from flask import Flask, request, jsonify
from flask_cors import CORS
import models
from datetime import datetime
import os

app = Flask(__name__)

CORS(app, origins=[
    "https://chess-microservices.vercel.app",
    "http://localhost:3000",
    "https://*.onrender.com"  # Permitir chamadas entre serviços Render
])

models.init_db()

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar se o serviço está funcionando"""
    return jsonify({'status': 'History Service is running!'}), 200

@app.route('/history/games', methods=['POST'])
def save_game():
    """
    Salva uma partida no histórico
    Body: {
        "game_id": "uuid",
        "mode": "local" | "ai",
        "white_player_id": 1,
        "black_player_id": 2,
        "winner": "white" | "black" | null,
        "status": "checkmate" | "stalemate" | "resigned",
        "moves_count": 25,
        "duration_seconds": 300,
        "pgn": "1. e4 e5 2. Nf3..."
    }
    """
    data = request.json
    
    if not data or not data.get('game_id'):
        return jsonify({'error': 'game_id is required'}), 400
    
    try:
        history_id = models.save_game_history(
            game_id=data['game_id'],
            mode=data.get('mode', 'local'),
            white_player_id=data.get('white_player_id'),
            black_player_id=data.get('black_player_id'),
            winner=data.get('winner'),
            status=data.get('status', 'completed'),
            moves_count=data.get('moves_count', 0),
            duration_seconds=data.get('duration_seconds', 0),
            pgn=data.get('pgn', '')
        )
        
        return jsonify({
            'success': True,
            'history_id': history_id,
            'message': 'Game saved to history'
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history/users/<int:user_id>', methods=['GET'])
def get_user_history(user_id):
    """
    Busca histórico de partidas de um usuário
    """
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    try:
        games = models.get_user_games(user_id, limit, offset)
        stats = models.get_user_stats(user_id)
        
        games_list = []
        for game in games:
            games_list.append({
                'id': game['id'],
                'game_id': game['game_id'],
                'mode': game['mode'],
                'opponent_id': game['black_player_id'] if game['white_player_id'] == user_id else game['white_player_id'],
                'player_color': 'white' if game['white_player_id'] == user_id else 'black',
                'result': game['winner'],
                'status': game['status'],
                'moves_count': game['moves_count'],
                'duration': game['duration_seconds'],
                'played_at': game['created_at']
            })
        
        return jsonify({
            'user_id': user_id,
            'games': games_list,
            'stats': stats,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'total': len(games_list)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history/games/<game_id>', methods=['GET'])
def get_game_history(game_id):
    """Busca detalhes de uma partida específica"""
    try:
        game = models.get_game_history(game_id)
        
        if not game:
            return jsonify({'error': 'Game not found'}), 404
        
        return jsonify({
            'game_id': game['game_id'],
            'mode': game['mode'],
            'white_player_id': game['white_player_id'],
            'black_player_id': game['black_player_id'],
            'winner': game['winner'],
            'status': game['status'],
            'moves_count': game['moves_count'],
            'duration_seconds': game['duration_seconds'],
            'pgn': game['pgn'],
            'played_at': game['created_at']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history/users/<int:user_id>/stats', methods=['GET'])
def get_user_stats_route(user_id):
    """Retorna estatísticas de um usuário"""
    try:
        stats = models.get_user_stats(user_id)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history/recent', methods=['GET'])
def get_recent_games():
    """Retorna partidas recentes"""
    limit = request.args.get('limit', 50, type=int)
    
    try:
        games = models.get_recent_games(limit)
        
        games_list = []
        for game in games:
            games_list.append({
                'game_id': game['game_id'],
                'mode': game['mode'],
                'white_player_id': game['white_player_id'],
                'black_player_id': game['black_player_id'],
                'winner': game['winner'],
                'status': game['status'],
                'moves_count': game['moves_count'],
                'played_at': game['created_at']
            })
        
        return jsonify({
            'games': games_list,
            'total': len(games_list)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8005))
    app.run(host='0.0.0', port=port, debug=False)  # debug=False para produção