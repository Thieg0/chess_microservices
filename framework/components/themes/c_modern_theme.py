from framework.interfaces.i_board_theme import IBoardTheme

# Componente concreto de tema visual: Moderno
# ESTA É UMA IMPLEMENTAÇÃO DE HOTSPOT: Define um visual moderno e limpo para o tabuleiro
class CModernTheme(IBoardTheme):

    # Retorna as cores das casas claras e escuras
    def get_board_colors(self) -> dict:
        return {"light": "#EEEED2", "dark": "#769656"}

    # Retorna o estilo das peças
    def get_piece_style(self) -> str:
        return "modern"

    # Retorna o nome amigável do tema
    def get_theme_name(self) -> str:
        return "Moderno"
