from framework.interfaces.i_game_mode import IGameMode

# Componente concreto de modo de jogo: Tutorial
# ESTA É UMA IMPLEMENTAÇÃO DE HOTSPOT: Modo assistido com dicas habilitadas
class CTutorialMode(IGameMode):

    # Retorna o nome do modo de jogo
    def get_mode_name(self) -> str:
        return "Tutorial"

    # Define se a IA está habilitada neste modo
    def is_ai_enabled(self) -> bool:
        return True

    # Retorna o número de jogadores humanos
    def get_player_count(self) -> int:
        return 1

    # Retorna as configurações específicas deste modo
    def get_mode_config(self) -> dict:
        return {"time_limit": None, "hints": True, "players": 1}
