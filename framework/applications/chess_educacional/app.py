from framework.chess_framework import ChessFramework
from framework.components.engines.c_minimax_engine import CMinimaxEngine
from framework.components.themes.c_colorful_theme import CColorfulTheme
from framework.components.modes.c_tutorial_mode import CTutorialMode
from framework.components.storage.c_sqlite_storage import CSQLiteStorage

# Aplicação 1 construída usando o FrameworkXadrez
# Usa Minimax (IA fraca) + Tema Colorido + Modo Tutorial
class XadrezEducacional(ChessFramework):

    # Define o tema colorido para a aplicação educacional
    def configurar_tema(self) -> None:
        self.theme = CColorfulTheme()

    # Define o modo tutorial (com dicas)
    def configurar_modo(self) -> None:
        self.game_mode = CTutorialMode()

    # Define o motor de busca Minimax
    def configurar_engine(self) -> None:
        self.engine = CMinimaxEngine()

    # Define o armazenamento em SQLite para persistência
    def configurar_storage(self) -> None:
        self.storage = CSQLiteStorage()

if __name__ == "__main__":
    # Instancia e inicializa a aplicação
    app = XadrezEducacional()
    config = app.iniciar_jogo()
    
    # Exibe as configurações resultantes da inicialização via Template Method
    print(f"Aplicação: {app.get_framework_info()}")
    print(f"Engine: {config['engine']}")
    print(f"Tema: {config['theme']}")
    print(f"Modo: {config['mode']}")
    print(f"Storage: {config['storage']}")
    print(f"IA habilitada: {config['ai_enabled']}")
    print(f"Jogadores: {config['player_count']}")
    print(f"Cores do tabuleiro: {config['board_colors']}")
    print(f"Config do modo: {config['mode_config']}")
