from ChessConstants import *


class Move:
    def __init__(
        self,
        start_square,
        end_square,
        piece,
        promoteTo=None,
        castle=NO_CASTLING,
        captured_piece=EMPTY,
    ) -> None:
        self.start_square = start_square
        self.end_square = end_square
        self.piece = piece
        self.promoteTo = promoteTo
        self.castle = castle
        self.captured_piece = captured_piece

    def __repr__(self) -> str:
        if self.castle != NO_CASTLING:
            if self.castle in [KINGSIDE_CASTLING[BLACK], KINGSIDE_CASTLING[WHITE]]:
                return "O-O"
            else:
                return "O-O-O"
        start_square = idx_to_square(self.start_square)
        end_square = idx_to_square(self.end_square)
        piece = PIECE_TO_TEXT[self.piece]
        return_string = f"{piece} {start_square} {end_square}"
        if self.promoteTo:
            return_string = f"{return_string} {PIECE_TO_TEXT[self.promoteTo]}"
        if self.captured_piece != EMPTY:
            return_string = (
                return_string + " Capturing " + PIECE_TO_TEXT[self.captured_piece]
            )
        return return_string
