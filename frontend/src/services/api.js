import axios from 'axios';

// URL do API Gateway (localhost em desenvolvimento)
const API_URL = process.env.REACT_APP_API_URL || 'https://chess-api-gateway.onrender.com';

console.log("API URL:", API_URL);

// Instância do axios configurada
const api = axios.create({
  baseURL: API_URL,
  timeout: 90000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token em todas as requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// ============= AUTH =============

export const register = async (name, email, password) => {
  try {
    const response = await api.post('/auth/register', {
      name,
      email,
      password,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Registration failed' };
  }
};

export const login = async (email, password) => {
  try {
    const response = await api.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Login failed' };
  }
};

// ============= GAME =============

export const createGame = async (mode, whitePlayerId, blackPlayerId = null) => {
  try {
    const response = await api.post('/games', {
      mode, // 'local' ou 'ai'
      white_player_id: whitePlayerId,
      black_player_id: blackPlayerId,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to create game' };
  }
};

export const getGame = async (gameId) => {
  try {
    const response = await api.get(`/games/${gameId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to get game' };
  }
};

export const makeMove = async (gameId, from, to, promotion = null) => {
  const payload = {
    from,
    to,
  };

  if (promotion) {
    payload.promotion = promotion;
  }
  
  console.log("=== MAKEMOVE DEBUG ===");
  console.log("Payload:", payload);
  console.log("URL:", `/games/${gameId}/move`);
  console.log("GameId:", gameId);
  console.log("From:", from);
  console.log("To:", to);
  console.log("Promotion:", promotion);
  console.log("Token:", localStorage.getItem('token')?.substring(0, 20) + "...");
  console.log("======================");
  
  try {
    const response = await api.post(`/games/${gameId}/move`, payload);
    console.log("SUCCESS:", response.data);
    return response.data;
  } catch (error) {
    console.error("ERROR completo:", error);
    console.error("ERROR response:", error.response?.data);
    console.error("ERROR status:", error.response?.status);
    console.error("ERROR request:", error.config);
    throw error.response?.data || { error: 'Invalid move' };
  }
};
export const resignGame = async (gameId, color) => {
  try {
    const response = await api.post(`/games/${gameId}/resign`, {
      color,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to resign' };
  }
};

export const getValidMoves = async (gameId, square = null) => {
  try {
    const url = square ? `/games/${gameId}/valid-moves?square=${square}` : `/games/${gameId}/valid-moves`;
    const response = await api.get(url);
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to get valid moves' };
  }
};

export const getAIMove = async (fen, difficulty = 'medium') => {
  try {
    const response = await api.post('/ai/move', {
      fen,
      difficulty,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to get AI move' };
  }
};

export const getHint = async (fen) => {
  try {
    const response = await api.post('/ai/hint', {
      fen,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || { error: 'Failed to get hint' };
  }
};

export default api;