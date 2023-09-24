from ChessConstants import *


class Move:
    def __init__(self, start_square, end_square, piece) -> None:
        self.start_square = start_square
        self.end_square = end_square
        self.piece = piece

    def get_start_square(self):
        return self.start_square

    def get_end_square(self):
        return self.end_square

    def get_piece(self):
        return self.piece

    def set_start_square(self, start_square):
        self.start_square = start_square

    def set_end_square(self, end_square):
        self.end_square = end_square

    def set_piece(self, piece):
        self.piece = piece

    def __repr__(self) -> str:
        start_square = idx_to_square(self.start_square)
        end_square = idx_to_square(self.end_square)
        piece = PIECE_TO_TEXT[self.piece]
        return f"{piece} {start_square} {end_square}"
