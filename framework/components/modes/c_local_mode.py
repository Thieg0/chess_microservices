from framework.interfaces.i_game_mode import IGameMode

# Componente concreto de modo de jogo: Local
# ESTA É UMA IMPLEMENTAÇÃO DE HOTSPOT: Define a lógica para partidas entre dois humanos no mesmo dispositivo
class CLocalMode(IGameMode):

    # Retorna o nome do modo de jogo
    def get_mode_name(self) -> str:
        return "Local"

    # Define se a IA está habilitada neste modo
    def is_ai_enabled(self) -> bool:
        return False

    # Retorna o número de jogadores humanos
    def get_player_count(self) -> int:
        return 2

    # Retorna as configurações específicas deste modo
    def get_mode_config(self) -> dict:
        return {"time_limit": None, "hints": False, "players": 2}
