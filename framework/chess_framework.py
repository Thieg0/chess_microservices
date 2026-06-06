from abc import ABC, abstractmethod
from framework.interfaces.i_chess_engine import IChessEngine
from framework.interfaces.i_board_theme import IBoardTheme
from framework.interfaces.i_game_mode import IGameMode
from framework.interfaces.i_storage_strategy import IStorageStrategy

# Classe base do framework que implementa o padrão Template Method
# ESTE É O NÚCLEO DO FRAMEWORK: Define a estrutura comum para todos os aplicativos de xadrez
class ChessFramework(ABC):

    def __init__(self):
        # Componentes que serão definidos pelos hotspots
        self.engine: IChessEngine = None
        self.theme: IBoardTheme = None
        self.game_mode: IGameMode = None
        self.storage: IStorageStrategy = None
        self.game_config: dict = {}

    # TEMPLATE METHOD: Define o algoritmo fixo de inicialização do jogo
    # FROZEN SPOT: Este método não deve ser sobrescrito pelas subclasses
    def iniciar_jogo(self) -> dict:
        self.configurar_tema()
        self.configurar_modo()
        self.configurar_engine()
        self.configurar_storage()
        return self.executar_configuracoes()

    # HOTSPOT: Define qual tema visual será utilizado
    @abstractmethod
    def configurar_tema(self) -> None:
        pass

    # HOTSPOT: Define o modo de jogo (Local, Online, IA)
    @abstractmethod
    def configurar_modo(self) -> None:
        pass

    # HOTSPOT: Define o motor de xadrez (Stockfish, Engine simples, etc)
    @abstractmethod
    def configurar_engine(self) -> None:
        pass

    # HOTSPOT: Define a estratégia de armazenamento (SQLite, Memória)
    @abstractmethod
    def configurar_storage(self) -> None:
        pass

    # FROZEN SPOT: Método concreto que consolida as configurações definidas
    def executar_configuracoes(self) -> dict:
        return {
            "engine": self.engine.get_engine_name(),
            "theme": self.theme.get_theme_name(),
            "mode": self.game_mode.get_mode_name(),
            "storage": self.storage.get_storage_name(),
            "ai_enabled": self.game_mode.is_ai_enabled(),
            "player_count": self.game_mode.get_player_count(),
            "board_colors": self.theme.get_board_colors(),
            "mode_config": self.game_mode.get_mode_config()
        }

    # FROZEN SPOT: Retorna informações básicas do framework
    def get_framework_info(self) -> str:
        return "FrameworkXadrez v1.0 - UFAL 2026"
