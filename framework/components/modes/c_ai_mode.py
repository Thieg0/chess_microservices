from framework.interfaces.i_game_mode import IGameMode

# Componente concreto de modo de jogo: vs IA
# ESTA É UMA IMPLEMENTAÇÃO DE HOTSPOT: Define a lógica para partidas contra o computador
class CAIMode(IGameMode):

    # Retorna o nome do modo de jogo
    def get_mode_name(self) -> str:
        return "vs IA"

    # Define se a IA está habilitada neste modo
    def is_ai_enabled(self) -> bool:
        return True

    # Retorna o número de jogadores humanos
    def get_player_count(self) -> int:
        return 1

    # Retorna as configurações específicas deste modo
    def get_mode_config(self) -> dict:
        return {"time_limit": None, "hints": False, "players": 1}
