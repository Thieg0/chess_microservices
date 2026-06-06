from framework.interfaces.i_board_theme import IBoardTheme

# Componente concreto de tema visual: Clássico
# ESTA É UMA IMPLEMENTAÇÃO DE HOTSPOT: Define as cores tradicionais de um tabuleiro de xadrez
class CClassicTheme(IBoardTheme):

    # Retorna as cores das casas claras e escuras
    def get_board_colors(self) -> dict:
        return {"light": "#F0D9B5", "dark": "#B58863"}

    # Retorna o estilo das peças
    def get_piece_style(self) -> str:
        return "classic"

    # Retorna o nome amigável do tema
    def get_theme_name(self) -> str:
        return "Clássico"
