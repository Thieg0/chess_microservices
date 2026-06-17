## Autor
Thiego Macena Santos

## Observacao
Este modulo foi desenvolvido individualmente
para as disciplinas de Reuso de Software e
Topicos em Engenharia de Software (2026).
O projeto base foi desenvolvido em conjunto
com Jayme Vinicius na disciplina de
Engenharia de Software (2025).

# Linha de Produto de Software - Topicos em Engenharia de Software

Documentacao da Linha de Produto de Software (LPS) desenvolvida para a disciplina de Topicos em Engenharia de Software, sob orientacao do Prof. Dr. Arturo Hernandez Dominguez no Instituto de Computacao da UFAL.

## Variabilidades da LPS

### Modo de Jogo (Selecao Alternativa)
- **Local**: Interacao entre dois jogadores humanos no mesmo terminal.
- **vs IA**: Interacao entre um jogador humano e o motor de inteligencia artificial.
- **Tutorial**: Modo pedagogico com assistencia por sistema de dicas.
- **Multiplayer Online**: Interacao remota em tempo real via protocolo WebSocket.

### Tema Visual (Selecao Alternativa)
- **Classico**: Esquema de cores tradicional (#F0D9B5 e #B58863).
- **Moderno**: Esquema de cores contemporaneo (#EEEED2 e #769656).
- **Colorido**: Esquema de cores de alto contraste (#FFE4B5 e #9370DB).

### Dificuldade da Inteligencia Artificial (Selecao Alternativa)
- **Facil**: Parametrizacao do Stockfish com profundidade 5 e nivel de habilidade 5.
- **Medio**: Parametrizacao do Stockfish com profundidade 10 e nivel de habilidade 10.
- **Dificil**: Parametrizacao do Stockfish com profundidade 15 e nivel de habilidade 20.

### Funcionalidades Opcionais
- Sistema de Dicas (exclusivo para o modo Tutorial).
- Historico de Partidas.
- Sistema de Recomendacao Personalizada.

## Produtos Derivados da LPS

### Xadrez Casual
- Modo: vs IA.
- Tema: Colorido.
- Dificuldade: Facil.
- Funcionalidades: Recomendacao e Historico.

### Xadrez Competitivo
- Modo: Multiplayer Online.
- Tema: Classico.
- Dificuldade: Nao aplicavel.
- Funcionalidades: Historico.

### Xadrez Educacional
- Modo: Tutorial.
- Tema: Colorido.
- Dificuldade: Facil.
- Funcionalidades: Dicas, Recomendacao e Historico.

## Microservicos da Arquitetura

### Recommendation Service (Porta 8006)
Modulo responsavel pela analise preditiva de dificuldade e modo de jogo com base no historico do usuario:
- Win rate >= 70%: Sugestao de dificuldade Dificil.
- Win rate >= 40%: Sugestao de dificuldade Medio.
- Win rate < 40%: Sugestao de dificuldade Facil.
- Prevalencia de partidas vs IA: Sugestao de modo vs IA.
- Prevalencia de partidas Locais: Sugestao de modo Local.

Endpoint de Consulta: `GET /recommendations/<user_id>`

### Multiplayer Service (Porta 8007)
Modulo de orquestracao de partidas em rede utilizando a biblioteca Socket.IO.

Principais Eventos:
- create_room: Inicializacao de sessao de jogo.
- join_room: Admissao em sessao existente.
- make_move: Transmissao de jogada para o servidor.
- move_made: Recebimento de jogada do oponente.
- game_started: Sinalizacao de inicio de partida.
- opponent_disconnected: Notificacao de interrupcao de conectividade.

## Persistencia de Dados (PostgreSQL)

O sistema utiliza PostgreSQL para armazenamento persistente das seguintes entidades:
- **users**: Registro e credenciais de usuarios.
- **games**: Estado corrente das sessoes de jogo.
- **moves**: Registro sequencial de movimentos.
- **game_history**: Dados agregados para o motor de recomendacao.

## Documentacao Grafica
Os diagramas detalhados de modelo de features, variabilidade e arquitetura estao disponiveis na pasta `docs/diagrams/`.

## Instancias em Producao
- Interface de Usuario: https://chess-microservices.vercel.app
- API Gateway: https://chess-api-gateway-s4wz.onrender.com
