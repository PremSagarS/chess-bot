from ChessGameState import ChessGameState
from ChessConstants import *
from Move import *

PIECE_VALUES = {PAWN: 100, KNIGHT: 300, BISHOP: 320, ROOK: 500, QUEEN: 900}


class ChessBot:
    def __init__(self, board: ChessGameState) -> None:
        self.board = board
        self.evaluatedCount = 0
        self.best_move: Move = None

    def countMaterialFor(self, color):
        pieces = PIECE_VALUES.keys()
        count = 0
        for piece in pieces:
            count += len(self.board.pieces[color | piece]) * PIECE_VALUES[piece]
        return count

    def evaluate(self):
        whiteMaterial = self.countMaterialFor(WHITE)
        blackMaterial = self.countMaterialFor(BLACK)

        evaluation = whiteMaterial - blackMaterial
        self.evaluatedCount += 1
        return evaluation if self.board.to_move == WHITE else -evaluation

    def move_value(self, move: Move) -> int:
        value = 0
        capturedPieceType = move.captured_piece & 0b00111
        movingPieceType = move.piece & 0b00111
        self.board.make_move(move)
        if self.board.is_in_check():
            value += 20
        self.board.unmake_last_move()
        if move.captured_piece != EMPTY:
            if movingPieceType == KING:
                value += PIECE_VALUES[capturedPieceType]
            else:
                value += PIECE_VALUES[capturedPieceType] - PIECE_VALUES[movingPieceType]
        return value

    def search(self, depth, setBestMove, alpha=float("-inf"), beta=float("inf")):
        if depth == 0:
            return self.evaluate()

        moves = self.board.generate_legal_moves()

        if moves == []:
            if self.board.is_in_check():
                return float("-inf")
            else:
                return 0

        moves.sort(key=self.move_value, reverse=True)

        for move in moves:
            if setBestMove:
                pass
            self.board.make_move(move)
            evaluation = -self.search(depth - 1, False, -beta, -alpha)
            self.board.unmake_last_move()
            if evaluation >= beta:
                if setBestMove:
                    self.best_move = move
                return beta
            if alpha < evaluation and setBestMove:
                self.best_move = move
            alpha = max(alpha, evaluation)

        return alpha
