# ♟️ Chess Microservices - Jogo de Xadrez Online

![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18-61DAFB)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![License](https://img.shields.io/badge/License-MIT-green)

Sistema de jogo de xadrez online desenvolvido com arquitetura de microserviços, utilizando Python (Flask) no backend e React no frontend. Projeto desenvolvido para a disciplina de Engenharia de Software da UFAL.

<p align="center">
  https://chess-microservices.vercel.app/
</p>

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Funcionalidades](#-funcionalidades)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [API Endpoints](#-api-endpoints)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Testes](#-testes)
- [Autores](#-autores)
- [Licença](#-licença)

---

## 🎬 Demonstração em Vídeo

<p align="center">
  <a href="https://youtu.be/SmCs-MtwpBM">
    <img src="https://img.youtube.com/vi/SmCs-MtwpBM/maxresdefault.jpg" alt="Vídeo Demonstração" width="700"/>
  </a>
</p>

<p align="center">
  <a href="https://youtu.be/SmCs-MtwpBM">
    <img src="https://img.shields.io/badge/▶️_Assistir_no_YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Assistir no YouTube"/>
  </a>
</p>

**O que você verá no vídeo:**
- ✅ Sistema completo funcionando
- ✅ Demonstração de autenticação
- ✅ Partidas vs jogador e vs IA
- ✅ Xeque-mate e validações

---

## 🎯 Sobre o Projeto

Este projeto implementa um jogo de xadrez completo seguindo os princípios de arquitetura de microserviços. O sistema permite que usuários:

- 🔐 Criem contas e façam login com autenticação JWT
- ♟️ Joguem xadrez contra outro jogador (modo local)
- 🤖 Joguem contra uma IA baseada no engine Stockfish (3 níveis de dificuldade)
- 📊 Visualizem histórico de partidas e estatísticas
- ✅ Tenham todas as regras oficiais do xadrez validadas

### Objetivos Pedagógicos

- Aplicar conceitos de **arquitetura de microserviços**
- Implementar **padrão API Gateway**
- Utilizar **autenticação JWT** e **bcrypt** para segurança
- Trabalhar com **containerização Docker**
- Praticar **metodologia ágil Scrum**

---

## 🏗️ Arquitetura

O sistema é composto por **5 microserviços** independentes que se comunicam via REST API:
```
                    ┌─────────────────┐
                    │   Frontend      │
                    │   (React)       │
                    │   Port 3000     │
                    └────────┬────────┘
                             │
                             ↓
                    ┌─────────────────┐
                    │  API Gateway    │
                    │   (Flask)       │
                    │   Port 8000     │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            ↓                ↓                ↓
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Auth Service │  │ Game Service │  │  AI Service  │
    │   Port 8001  │  │   Port 8003  │  │  Port 8004   │
    └──────────────┘  └──────────────┘  └──────────────┘
                             │
                             ↓
                    ┌──────────────────┐
                    │ History Service  │
                    │    Port 8005     │
                    └──────────────────┘
```

### Microserviços

#### 🚪 **API Gateway (Port 8000)**
- Ponto único de entrada
- Roteamento de requisições
- Validação de tokens JWT
- Tratamento de erros

#### 🔐 **Auth Service (Port 8001)**
- Registro de usuários
- Login e autenticação
- Geração e validação de tokens JWT
- Criptografia de senhas com bcrypt

#### ♟️ **Game Service (Port 8003)**
- Lógica do jogo de xadrez
- Validação de movimentos
- Detecção de xeque, xeque-mate, empate
- Gerenciamento de estado do tabuleiro
- Utiliza biblioteca `python-chess`

#### 🤖 **AI Service (Port 8004)**
- Implementação do oponente computadorizado
- Engine Stockfish (ELO 3500+)
- 3 níveis de dificuldade (Easy, Medium, Hard)
- Sistema de dicas

#### 📜 **History Service (Port 8005)**
- Armazenamento de histórico de partidas
- Cálculo de estatísticas
- Consultas de partidas anteriores

---

## 🛠️ Tecnologias

### Backend
- **Python 3.11+** - Linguagem principal
- **Flask 3.0** - Framework web
- **python-chess 1.999** - Validação de regras do xadrez
- **Stockfish** - Engine de IA
- **PyJWT 2.8** - Geração de tokens JWT
- **bcrypt 4.1** - Criptografia de senhas
- **SQLite3** - Banco de dados

### Frontend
- **React 18** - Biblioteca UI
- **chess.js** - Validação de movimentos no cliente
- **react-chessboard 4.3** - Componente de tabuleiro
- **Axios 1.6** - Cliente HTTP

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers

### Arquitetura
- **Microserviços** - Separação de responsabilidades
- **REST API** - Comunicação HTTP
- **JWT** - Autenticação stateless
- **API Gateway Pattern** - Centralização

---

## ✨ Funcionalidades

### Autenticação
- ✅ Registro de usuários
- ✅ Login com JWT
- ✅ Tokens com expiração de 24h
- ✅ Senhas criptografadas com bcrypt

### Jogo
- ✅ Modo 2 jogadores local
- ✅ Modo vs IA (Easy/Medium/Hard)
- ✅ Validação completa das regras oficiais
- ✅ Detecção de xeque e xeque-mate
- ✅ Detecção de empate (afogamento, material insuficiente)
- ✅ Promoção de peões
- ✅ Drag and drop intuitivo
- ✅ Indicadores visuais de status

### Histórico
- ✅ Armazenamento de partidas
- ✅ Estatísticas de vitórias/derrotas
- ✅ Taxa de vitória
- ✅ Consulta de partidas anteriores

---

## 📦 Pré-requisitos

Antes de começar, você precisa ter instalado:

- [Docker](https://docs.docker.com/get-docker/) (versão 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (versão 2.0+)
- [Git](https://git-scm.com/)

**Opcional (para desenvolvimento sem Docker):**
- Python 3.11+
- Node.js 18+
- Stockfish

---

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/Thieg0/chess_microservices.git
cd chess_microservices
```

### 2. Inicie os containers
```bash
docker-compose up -d
```

Isso vai:
- ✅ Construir as imagens Docker
- ✅ Iniciar todos os microserviços
- ✅ Criar a rede interna
- ✅ Configurar volumes persistentes

### 3. Aguarde os serviços iniciarem
```bash
docker-compose ps
```

Todos os serviços devem estar com status `Up`:
```
NAME                    STATUS
chess-api-gateway       Up
chess-auth-service      Up
chess-game-service      Up
chess-ai-service        Up
chess-history-service   Up
chess-frontend          Up
```

### 4. Acesse a aplicação

Abra seu navegador em: **http://localhost:3000**

---

## 📖 Como Usar

### Primeiro acesso

1. **Crie uma conta**
   - Clique em "Criar Conta"
   - Preencha: Nome, Email, Senha (mínimo 6 caracteres)
   - Clique em "Registrar"

2. **Faça login**
   - Use o email e senha cadastrados
   - Você será redirecionado para o jogo

### Jogar

#### Modo 2 Jogadores Local
1. Clique em "Novo Jogo"
2. Selecione "👥 2 Jogadores Local"
3. Arraste as peças para movê-las
4. As brancas começam

#### Modo vs IA
1. Clique em "Novo Jogo"
2. Escolha a dificuldade:
   - 🤖 IA Fácil (profundidade 5)
   - 🤖 IA Médio (profundidade 10)
   - 🤖 IA Difícil (profundidade 15)
3. Você joga com as peças brancas
4. A IA responde automaticamente

### Outras funcionalidades

- **Desfazer Jogada**: Volta o último movimento (apenas local)
- **Mudar Cor das Peças**: Inverte o tabuleiro
- **Sair**: Faz logout

---

## 🔌 API Endpoints

### Authentication
```http
POST /auth/register
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao@email.com",
  "password": "senha123"
}

Response: 201 Created
{
  "user_id": 1,
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```
```http
POST /auth/login
Content-Type: application/json

{
  "email": "joao@email.com",
  "password": "senha123"
}

Response: 200 OK
{
  "user_id": 1,
  "name": "João Silva",
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Game
```http
POST /games
Authorization: Bearer <token>
Content-Type: application/json

{
  "mode": "local",
  "white_player_id": 1,
  "black_player_id": 1
}

Response: 201 Created
{
  "game_id": "550e8400-e29b-41d4-a716-446655440000",
  "board_state": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "current_turn": "white",
  "status": "active"
}
```
```http
POST /games/{game_id}/move
Authorization: Bearer <token>
Content-Type: application/json

{
  "from": "e2",
  "to": "e4",
  "promotion": null
}

Response: 200 OK
{
  "success": true,
  "board_state": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
  "current_turn": "black",
  "is_check": false,
  "is_checkmate": false
}
```

### AI
```http
POST /ai/move
Authorization: Bearer <token>
Content-Type: application/json

{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "difficulty": "medium"
}

Response: 200 OK
{
  "success": true,
  "move": {
    "from": "e2",
    "to": "e4",
    "promotion": null,
    "uci": "e2e4",
    "san": "e4"
  },
  "difficulty": "medium"
}
```

### History
```http
GET /history/users/{user_id}
Authorization: Bearer <token>

Response: 200 OK
{
  "user_id": 1,
  "games": [...],
  "stats": {
    "total_games": 10,
    "wins": 6,
    "losses": 3,
    "draws": 1,
    "win_rate": 60.0
  }
}
```

**Documentação completa da API:** [docs/API.md](docs/API.md)

---

## 📁 Estrutura do Projeto
```
chess_microservices/
├── api-gateway/
│   ├── app.py              # Ponto de entrada
│   ├── gateway.py          # Lógica de roteamento
│   ├── Dockerfile
│   └── requirements.txt
│
├── services/
│   ├── auth-service/
│   │   ├── app.py          # Rotas de autenticação
│   │   ├── auth.py         # JWT utils
│   │   ├── models.py       # Banco de dados
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── game-service/
│   │   ├── app.py          # Rotas do jogo
│   │   ├── game_logic.py   # Lógica do xadrez
│   │   ├── models.py       # Banco de dados
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── ai-service/
│   │   ├── app.py          # Rotas da IA
│   │   ├── ai_engine.py    # Integração Stockfish
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── history-service/
│       ├── app.py          # Rotas de histórico
│       ├── models.py       # Banco de dados
│       ├── Dockerfile
│       └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Componente principal
│   │   ├── ChessBoard.jsx  # Componente do tabuleiro
│   │   └── services/
│   │       └── api.js      # Cliente HTTP
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml      # Orquestração
├── README.md
└── docs/
    ├── API.md
    └── ARCHITECTURE.md
```

---

## 🧪 Testes

### Testes Automatizados

Execute o script de testes que valida o fluxo completo:
```bash
./test_api.sh
```

O script testa:
1. ✅ Health check do API Gateway
2. ✅ Registro de novo usuário
3. ✅ Login e obtenção de token
4. ✅ Criação de jogo
5. ✅ Execução de movimento

### Testes Manuais

#### Testar Auth Service
```bash
# Health check
curl http://localhost:8001/health

# Registrar usuário
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"123456"}'
```

#### Testar Game Service
```bash
# Health check
curl http://localhost:8003/health
```

#### Testar AI Service
```bash
# Health check
curl http://localhost:8004/health

# Verificar se Stockfish está disponível
docker exec chess-ai-service stockfish --version
```

---

## 🐛 Troubleshooting

### Problema: Containers não iniciam
```bash
# Ver logs de um serviço específico
docker-compose logs auth-service

# Ver logs de todos
docker-compose logs

# Reconstruir imagens
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Porta já em uso
```bash
# Verificar o que está usando a porta
lsof -i :8000
lsof -i :3000

# Parar o processo ou mudar a porta no docker-compose.yml
```

### Problema: AI Service não funciona
```bash
# Verificar se Stockfish está instalado
docker exec chess-ai-service which stockfish

# Se não estiver, reconstruir a imagem
docker-compose build ai-service
```

### Problema: Banco de dados corrompido
```bash
# Remover volumes
docker-compose down -v

# Subir novamente
docker-compose up -d
```

---

## 🔧 Desenvolvimento

### Rodar sem Docker (desenvolvimento local)

#### Backend
```bash
# Auth Service
cd services/auth-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

### Configurar variáveis de ambiente

Crie um arquivo `.env`:
```env
# API URLs (para docker-compose)
AUTH_SERVICE_URL=http://auth-service:8001
GAME_SERVICE_URL=http://game-service:8003
AI_SERVICE_URL=http://ai-service:8004
HISTORY_SERVICE_URL=http://history-service:8005

# JWT Secret (MUDAR EM PRODUÇÃO!)
SECRET_KEY=seu-secret-key-super-secreto

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

---

## 📚 Documentação Adicional

- [Arquitetura Detalhada](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Guia de Contribuição](docs/CONTRIBUTING.md)
- [Relatório do Projeto](docs/Relatorio.pdf)

---

## 👥 Autores

- **Jayme Vinícius Esteves Pedroza Melo** - [GitHub](https://github.com/jaymevinicius)
- **Thiego Macena Santos** - [GitHub](https://github.com/Thieg0)

**Orientador:** Prof. Dr. Arturo Hernández Domínguez

**Instituição:** Universidade Federal de Alagoas (UFAL) - Instituto de Computação

**Disciplina:** Engenharia de Software

**Ano:** 2025.2

---

