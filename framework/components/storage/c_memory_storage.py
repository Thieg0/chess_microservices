from framework.interfaces.i_storage_strategy import IStorageStrategy

# Componente concreto de estratégia de armazenamento: Memória (Volátil)
# ESTA É UMA IMPLEMENTAÇÃO DE HOTSPOT: Fornece armazenamento rápido em memória para sessões temporárias
class CMemoryStorage(IStorageStrategy):

    def __init__(self):
        self.name = "Memória"
        self.games = {}  # Dicionário para armazenar jogos em tempo de execução

    # Salva os dados de uma partida no dicionário
    def save_game(self, game_data: dict) -> bool:
        game_id = game_data["game_id"]
        self.games[game_id] = game_data
        return True

    # Recupera uma partida do dicionário pelo ID
    def get_game(self, game_id: str) -> dict:
        return self.games.get(game_id, None)

    # Recupera o histórico filtrando os jogos do jogador na memória
    def get_player_history(self, player_id: int) -> list:
        history = [
            game for game in self.games.values() 
            if game.get("player_id") == player_id
        ]
        return history

    # Retorna o nome da estratégia de armazenamento
    def get_storage_name(self) -> str:
        return self.name
