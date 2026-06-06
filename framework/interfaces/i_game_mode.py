from abc import ABC, abstractmethod

# Interface para definição dos modos de jogo do framework
# ESTE É UM HOTSPOT: Deve ser estendido para criar novas variações de jogo
class IGameMode(ABC):

    # Retorna o nome do modo de jogo
    # HOTSPOT: Identificador do modo (ex: Local, Online, Treinamento)
    @abstractmethod
    def get_mode_name(self) -> str:
        pass

    # Indica se este modo utiliza inteligência artificial
    # HOTSPOT: Define se o sistema deve carregar um motor de IA
    @abstractmethod
    def is_ai_enabled(self) -> bool:
        pass

    # Retorna um dicionário com as configurações específicas do modo
    # HOTSPOT: Permite definir limites de tempo, permissão de dicas, etc
    @abstractmethod
    def get_mode_config(self) -> dict:
        pass

    # Retorna a quantidade de jogadores humanos participantes
    # HOTSPOT: Define se o jogo é para 1 ou 2 humanos
    @abstractmethod
    def get_player_count(self) -> int:
        pass
