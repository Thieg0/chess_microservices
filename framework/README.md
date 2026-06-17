# FrameworkXadrez - Reuso de Software

Framework desenvolvido para a disciplina de Reuso de Software e Metodologias Ageis, utilizando o padrao de projeto Template Method para promover a extensibilidade e o reuso de componentes de software.

## Padrao Utilizado
O sistema utiliza o padrao Template Method, definindo quatro hotspots (pontos de adaptacao) distintos e diversos frozen spots (partes invariantes que compoem o nucleo do framework).

## Estrutura do Projeto
- **chess_framework.py**: Classe abstrata primordial que define o esqueleto do algoritmo.
- **interfaces/**: Definicoes de contratos para os hotspots.
  - i_chess_engine.py: Hotspot para o Motor de IA.
  - i_board_theme.py: Hotspot para o Tema Visual.
  - i_game_mode.py: Hotspot para o Modo de Jogo.
  - i_storage_strategy.py: Hotspot para a Estrategia de Persistencia.
- **components/**: Implementacoes concretas disponiveis.
  - engines/: CStockfishEngine, CMinimaxEngine, CRandomEngine.
  - themes/: CClassicTheme, CModernTheme, CColorfulTheme.
  - modes/: CLocalMode, CAIMode, CTutorialMode.
  - storage/: CSQLiteStorage, CMemoryStorage.
- **applications/**: Exemplos de instanciacao do framework.
  - chess_educacional/: Aplicacao voltada ao ensino.
  - chess_torneio/: Aplicacao voltada a competicao.
- **demo/**: Interface para demonstracao das capacidades do framework.
- **marketplace/**: Catalogo de servicos e componentes integrados.

## Hotspots
| Hotspot | Interface | Componentes Disponiveis |
|---------|-----------|-------------|
| Motor de IA | IChessEngine | Stockfish, Minimax, Random |
| Tema Visual | IBoardTheme | Classic, Modern, Colorful |
| Modo de Jogo | IGameMode | Local, AI, Tutorial |
| Persistencia | IStorageStrategy | SQLite, Memory |

## Frozen Spots
- **iniciar_jogo()**: Metodo modelo que orquestra a inicializacao.
- **executar_configuracoes()**: Consolida as escolhas de design da aplicacao.
- **get_framework_info()**: Fornece metadados de identificacao do framework.
- **Regras do Xadrez**: Logica fundamental baseada na biblioteca python-chess.

## Procedimentos de Execucao

Para configurar o ambiente de execucao:
```bash
cd framework
python3 -m venv venv
source venv/bin/activate
pip install python-chess
```

Execucao da Aplicacao 1 (Xadrez Educacional):
```bash
python3 -m framework.applications.chess_educacional.app
```

Execucao da Aplicacao 2 (Xadrez Torneio):
```bash
python3 -m framework.applications.chess_torneio.app
```

## Desenvolvimento de Novas Aplicacoes

A criacao de uma nova aplicacao consiste em herdar da classe base e implementar os metodos abstratos:

```python
from framework.chess_framework import ChessFramework
from framework.components.engines.c_stockfish_engine import CStockfishEngine
from framework.components.themes.c_modern_theme import CModernTheme
from framework.components.modes.c_ai_mode import CAIMode
from framework.components.storage.c_sqlite_storage import CSQLiteStorage

class MinhaAplicacao(ChessFramework):
    def configurar_tema(self):
        self.theme = CModernTheme()

    def configurar_modo(self):
        self.game_mode = CAIMode()

    def configurar_engine(self):
        self.engine = CStockfishEngine()

    def configurar_storage(self):
        self.storage = CSQLiteStorage()

app = MinhaAplicacao()
config = app.iniciar_jogo()
print(config)
```

## Demonstracao e Marketplace
- Para visualizar as aplicacoes instanciadas, acesse `framework/demo/index.html` via navegador.
- O catalogo de microservicos pode ser consultado em `framework/marketplace/index.html`.
