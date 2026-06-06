from abc import ABC, abstractmethod

# Interface para definição de temas do tabuleiro
# ESTE É UM HOTSPOT: Deve ser estendido para criar novos estilos visuais
class IBoardTheme(ABC):

    # Retorna as cores das casas (light e dark)
    # HOTSPOT: Permite customizar a paleta de cores do tabuleiro
    @abstractmethod
    def get_board_colors(self) -> dict:
        pass

    # Retorna o estilo visual das peças
    # HOTSPOT: Define qual conjunto de imagens de peças será usado
    @abstractmethod
    def get_piece_style(self) -> str:
        pass

    # Retorna o nome amigável do tema
    # HOTSPOT: Nome que aparecerá na interface para o usuário
    @abstractmethod
    def get_theme_name(self) -> str:
        pass
