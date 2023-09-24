from ChessConstants import *


class Move:
    def __init__(
        self, start_square, end_square, piece, promoteTo=None, castle=NO_CASTLING
    ) -> None:
        self.start_square = start_square
        self.end_square = end_square
        self.piece = piece
        self.promoteTo = promoteTo
        self.castle = castle

    def __repr__(self) -> str:
        start_square = idx_to_square(self.start_square)
        end_square = idx_to_square(self.end_square)
        piece = PIECE_TO_TEXT[self.piece]
        return f"{piece} {start_square} {end_square}"
