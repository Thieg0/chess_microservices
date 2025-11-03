from flask import Flask, request, jsonify
from flask_cors import CORS
import ai_engine
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8004))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False para produção

app = Flask(__name__)

CORS(app, origins=[
    "https://chess-microservices.vercel.app",
    "http://localhost:3000",
    "https://*.onrender.com"  # Permitir chamadas entre serviços Render
])

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar se o serviço está funcionando"""
    return jsonify({'status': 'AI Service is running!'}), 200

@app.route('/ai/move', methods=['POST'])
def get_ai_move():
    """
    Retorna a melhor jogada calculada pela IA
    Body: {
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "difficulty": "easy" | "medium" | "hard" (opcional, padrão: medium)
    }
    """
    data = request.json
    
    if not data or not data.get('fen'):
        return jsonify({'error': 'FEN board state is required'}), 400
    
    fen = data['fen']
    difficulty = data.get('difficulty', 'medium')
    
    if difficulty not in ['easy', 'medium', 'hard']:
        return jsonify({'error': 'Difficulty must be easy, medium or hard'}), 400
    
    try:
        best_move = ai_engine.get_best_move(fen, difficulty)
        
        if not best_move:
            return jsonify({'error': 'No legal moves available or game is over'}), 400
        
        move_info = ai_engine.get_move_details(fen, best_move)
        
        return jsonify({
            'success': True,
            'move': {
                'from': best_move[:2],
                'to': best_move[2:4],
                'promotion': best_move[4] if len(best_move) > 4 else None,
                'uci': best_move,
                'san': move_info['san'],
                'piece': move_info['piece']
            },
            'difficulty': difficulty,
            'evaluation': move_info.get('evaluation'),
            'fen': fen
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai/hint', methods=['POST'])
def get_hint():
    """
    Retorna uma dica de movimento (melhor jogada)
    Body: {
        "fen": "..."
    }
    """
    data = request.json
    
    if not data or not data.get('fen'):
        return jsonify({'error': 'FEN board state is required'}), 400
    
    fen = data['fen']
    
    try:
        best_move = ai_engine.get_best_move(fen, 'hard')
        
        if not best_move:
            return jsonify({'error': 'No legal moves available'}), 400
        
        move_info = ai_engine.get_move_details(fen, best_move)
        
        return jsonify({
            'success': True,
            'hint': {
                'from': best_move[:2],
                'to': best_move[2:4],
                'san': move_info['san'],
                'piece': move_info['piece']
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🤖 Starting AI Service on port 8004...")
    print("Initializing Stockfish engine...")
    
    if not ai_engine.is_stockfish_available():
        print("⚠️  WARNING: Stockfish not found! AI will use fallback random moves.")
        print("Install Stockfish: apt-get install stockfish")
    else:
        print("✅ Stockfish engine ready!")
    
    app.run(host='0.0.0.0', port=8004, debug=True)