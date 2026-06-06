from framework.interfaces.i_board_theme import IBoardTheme

# Componente concreto de tema visual: Colorido
# ESTA É UMA IMPLEMENTAÇÃO DE HOTSPOT: Fornece uma opção vibrante e diferenciada de cores
class CColorfulTheme(IBoardTheme):

    # Retorna as cores das casas claras e escuras
    def get_board_colors(self) -> dict:
        return {"light": "#FFE4B5", "dark": "#9370DB"}

    # Retorna o estilo das peças
    def get_piece_style(self) -> str:
        return "colorful"

    # Retorna o nome amigável do tema
    def get_theme_name(self) -> str:
        return "Colorido"
