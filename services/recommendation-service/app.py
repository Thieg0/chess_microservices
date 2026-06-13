from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get('DATABASE_URL')
HISTORY_SERVICE_URL = os.environ.get('HISTORY_SERVICE_URL', 'http://localhost:8005')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Recommendation Service is running!"}), 200

@app.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT COUNT(*) as total,
            SUM(CASE WHEN (white_player_id=%s AND winner='white') 
                     OR (black_player_id=%s AND winner='black') 
                     THEN 1 ELSE 0 END) as wins,
            SUM(CASE WHEN mode='ai' THEN 1 ELSE 0 END) as ai_games,
            SUM(CASE WHEN mode='local' THEN 1 ELSE 0 END) as local_games
            FROM game_history
            WHERE white_player_id=%s OR black_player_id=%s
        """
        cur.execute(query, (user_id, user_id, user_id, user_id))
        stats = cur.fetchone()
        cur.close()
        conn.close()

        total = stats['total'] or 0
        wins = stats['wins'] or 0
        ai_games = stats['ai_games'] or 0
        local_games = stats['local_games'] or 0
        
        if total == 0:
            return jsonify({
                "user_id": user_id,
                "recommended_difficulty": "easy",
                "recommended_mode": "ai",
                "reason": "Bem-vindo! Comece com IA no modo fácil.",
                "stats": {"total_games": 0, "win_rate": 0, "ai_games": 0, "local_games": 0}
            }), 200

        win_rate = wins / total
        if win_rate >= 0.7:
            recommended_difficulty = "hard"
        elif win_rate >= 0.4:
            recommended_difficulty = "medium"
        else:
            recommended_difficulty = "easy"

        recommended_mode = "ai" if ai_games >= local_games else "local"

        return jsonify({
            "user_id": user_id,
            "recommended_difficulty": recommended_difficulty,
            "recommended_mode": recommended_mode,
            "reason": "Baseado no seu histórico de partidas",
            "stats": {
                "total_games": total,
                "win_rate": round(win_rate, 2),
                "ai_games": ai_games,
                "local_games": local_games
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8006))
    app.run(host='0.0.0.0', port=port, debug=False)
