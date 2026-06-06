from abc import ABC, abstractmethod

# Interface para definir a estratégia de armazenamento do framework
# ESTE É UM HOTSPOT: Deve ser implementada para suportar diferentes bancos de dados
class IStorageStrategy(ABC):

    # Salva os dados de uma partida no armazenamento
    # HOTSPOT: Define como os dados do jogo serão persistidos (JSON, SQL, etc)
    @abstractmethod
    def save_game(self, game_data: dict) -> bool:
        pass

    # Busca uma partida específica através do seu identificador único
    # HOTSPOT: Implementação da consulta de recuperação de dados
    @abstractmethod
    def get_game(self, game_id: str) -> dict:
        pass

    # Recupera a lista de todas as partidas de um determinado jogador
    # HOTSPOT: Filtro de busca por ID de jogador
    @abstractmethod
    def get_player_history(self, player_id: int) -> list:
        pass

    # Retorna o nome amigável do tipo de armazenamento utilizado
    # HOTSPOT: Identificador da estratégia (ex: "SQLite", "MongoDB", "Memória")
    @abstractmethod
    def get_storage_name(self) -> str:
        pass
