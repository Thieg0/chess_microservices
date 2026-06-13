from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import chess
import os
import uuid

app = Flask(__name__)
CORS(app, origins="*")
# Configura o SocketIO com eventlet para melhor performance em tempo real
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Salas de jogo em memória (neste protótipo não persistimos em DB)
rooms = {}
# Mapeamento do ID do socket para o ID da sala
player_rooms = {}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Multiplayer Service is running!"}), 200

@app.route('/rooms', methods=['GET'])
def get_rooms():
    """Retorna lista de salas aguardando jogadores"""
    available_rooms = [
        {"room_id": r_id, "status": r_data["status"]}
        for r_id, r_data in rooms.items()
        if r_data["status"] == "waiting"
    ]
    return jsonify(available_rooms), 200

@socketio.on('connect')
def handle_connect():
    print(f"Cliente conectado: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in player_rooms:
        room_id = player_rooms[sid]
        if room_id in rooms:
            # Notifica o oponente que o jogador saiu
            emit('opponent_disconnected', {"message": "Oponente desconectou"}, room=room_id)
            
            # Limpa a sala se ficar vazia ou o jogo acabar
            # Em uma implementação real, poderíamos ter um timer para reconexão
            leave_room(room_id)
            del player_rooms[sid]
            
            # Se não houver mais ninguém na sala (baseado no mapeamento), deleta a sala
            # Simplificação: deleta se algum sair
            if room_id in rooms:
                del rooms[room_id]
    print(f"Cliente desconectado: {sid}")

@socketio.on('create_room')
def handle_create_room(data):
    room_id = str(uuid.uuid4())[:8] # ID curto para facilitar
    rooms[room_id] = {
        "board": chess.Board(),
        "white": request.sid,
        "black": None,
        "status": "waiting"
    }
    player_rooms[request.sid] = room_id
    join_room(room_id)
    emit('room_created', {"room_id": room_id, "color": "white"})
    print(f"Sala {room_id} criada por {request.sid}")

@socketio.on('join_room')
def handle_join_room(data):
    room_id = data.get('room_id')
    if room_id in rooms and rooms[room_id]["status"] == "waiting":
        rooms[room_id]["black"] = request.sid
        rooms[room_id]["status"] = "playing"
        player_rooms[request.sid] = room_id
        join_room(room_id)
        
        # Notifica ambos que o jogo começou
        emit('game_started', {"color": "black", "room_id": room_id}, room=request.sid)
        emit('game_started', {"color": "white", "room_id": room_id}, room=rooms[room_id]["white"])
        print(f"Jogador {request.sid} entrou na sala {room_id}")
    else:
        emit('error', {"message": "Sala não encontrada ou cheia"})

@socketio.on('make_move')
def handle_make_move(data):
    room_id = data.get('room_id')
    if room_id not in rooms:
        return
    
    board = rooms[room_id]["board"]
    move_from = data.get('from')
    move_to = data.get('to')
    promotion = data.get('promotion')
    
    # Converte strings para objetos do python-chess
    try:
        move_str = f"{move_from}{move_to}"
        if promotion:
            move_str += promotion.lower()
        
        move = chess.Move.from_uci(move_str)
        
        if move in board.legal_moves:
            board.push(move)
            
            # Notifica todos na sala sobre o movimento
            emit('move_made', {
                "from": move_from,
                "to": move_to,
                "promotion": promotion,
                "fen": board.fen(),
                "turn": "white" if board.turn == chess.WHITE else "black",
                "is_check": board.is_check(),
                "is_checkmate": board.is_checkmate(),
                "is_stalemate": board.is_stalemate(),
                "last_move_uci": move_str
            }, room=room_id)
        else:
            emit('invalid_move', {"message": "Movimento ilegal"})
            
    except Exception as e:
        emit('invalid_move', {"message": f"Erro ao processar movimento: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8007))
    # socketio.run gerencia o servidor eventlet
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
