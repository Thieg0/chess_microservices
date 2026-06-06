from abc import ABC, abstractmethod

class IChessEngine(ABC):
    
    # Interface abstrata para motores de xadrez (Chess Engines).
    # HOTSPOT - deve ser implementado por cada aplicação que usar o framework com sua própria engine de IA.
    @abstractmethod
    def get_best_move(self, fen: str, difficulty: str) -> str:
        
        # Retorna o melhor movimento para a posição atual.
        # HOTSPOT: Implemente aqui o algoritmo de busca (ex: Stockfish, Minimax, MCTS).
        # fen (str): O estado do tabuleiro em formato FEN (Forsyth-Edwards Notation).
        # difficulty (str): Nível de dificuldade desejado ("easy", "medium", "hard").
        # Returns:
            # str: O movimento escolhido no formato UCI (ex: "e2e4", "g1f3").
        pass

    @abstractmethod
    def get_engine_name(self) -> str:
        """
        Retorna o nome identificador deste motor de xadrez.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Verifica se o motor e suas dependências estão prontos para uso.
        """
        pass
