from framework.chess_framework import ChessFramework
from framework.components.engines.c_stockfish_engine import CStockfishEngine
from framework.components.themes.c_classic_theme import CClassicTheme
from framework.components.modes.c_local_mode import CLocalMode
from framework.components.storage.c_sqlite_storage import CSQLiteStorage

# Aplicação 2 construída usando o FrameworkXadrez
# Usa Stockfish (IA forte) + Tema Clássico + Modo Local
class XadrezTorneio(ChessFramework):

    # Define o tema clássico (bege e marrom)
    def configurar_tema(self) -> None:
        self.theme = CClassicTheme()

    # Define o modo local (2 jogadores humanos)
    def configurar_modo(self) -> None:
        self.game_mode = CLocalMode()

    # Define o motor de alto desempenho Stockfish
    def configurar_engine(self) -> None:
        self.engine = CStockfishEngine()

    # Define o armazenamento em SQLite para persistência das partidas
    def configurar_storage(self) -> None:
        self.storage = CSQLiteStorage()

if __name__ == "__main__":
    # Instancia e inicializa a aplicação
    app = XadrezTorneio()
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
