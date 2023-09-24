from Move import Move
from ChessConstants import *


class ChessGameState:
    def __init__(self):
        self.chessboard = [0] * 64
        self.draw_move_counter = 0
        self.move_counter = 1
        self.fen_notations = []
        self.castling_rights = []
        self.en_passant_square = None
        self.moves = []
        self.pieces = [] * 23
        self.set_to_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        for i in range(23):
            self.pieces.append([])
        self.gen_pieces()
        self.numsquarestoedge = []
        for i in range(64):
            self.numsquarestoedge.append([])
        self.precomputemovedata()

    def precomputemovedata(self):
        for rank in range(8):
            for file in range(8):
                northMax = rank
                southMax = 7 - rank
                eastMax = 7 - file
                westMax = file

                square = rank * 8 + file

                self.numsquarestoedge[square] = [
                    northMax,
                    southMax,
                    eastMax,
                    westMax,
                    min(northMax, eastMax),
                    min(northMax, westMax),
                    min(southMax, eastMax),
                    min(southMax, westMax),
                ]

    def generate_pseudo_legal_moves_for(self, start_square_idx):
        startSquarePiece = self.chessboard[start_square_idx]
        startSquarePieceType = startSquarePiece & 0b00111
        startSquarePieceColor = startSquarePiece & 0b11000
        if startSquarePieceColor != self.to_move:
            return []

        possibleMoves = []

        directionIndexStart = directionIndexEnd = None

        if startSquarePieceType == BISHOP:
            directionIndexStart = 4
            directionIndexEnd = 7

        elif startSquarePieceType == ROOK:
            directionIndexStart = 0
            directionIndexEnd = 3

        elif startSquarePieceType == QUEEN:
            directionIndexStart = 0
            directionIndexEnd = 7

        for directionIndex in range(directionIndexStart, directionIndexEnd + 1):
            for n in range(
                1, self.numsquarestoedge[start_square_idx][directionIndex] + 1
            ):
                end_square_idx = start_square_idx + DIRECTIONOFFSETS[directionIndex] * n
                endSquarePiece = self.chessboard[end_square_idx]
                endSquareColor = endSquarePiece & 0b11000
                if endSquarePiece == EMPTY:
                    possibleMoves.append(
                        Move(start_square_idx, end_square_idx, startSquarePiece)
                    )
                elif endSquareColor == self.to_move:
                    break
                else:
                    possibleMoves.append(
                        Move(start_square_idx, end_square_idx, startSquarePiece)
                    )
        return possibleMoves

    def set_to_fen(self, fen):
        position, to_move, castling, passant, draw, move_no = fen.split(" ")
        index = 0
        for i in range(64):
            self.chessboard[i] = 0
        for character in position:
            if character.isdigit():
                index += int(character)
            elif character == "/":
                continue
            else:
                self.chessboard[index] = TEXT_TO_PIECE[character]
                index += 1
        if to_move == "w":
            self.to_move = WHITE
        else:
            self.to_move = BLACK
        self.castling_rights = [
            "K" in castling,
            "Q" in castling,
            "k" in castling,
            "q" in castling,
        ]
        if passant == "-":
            self.en_passant_square = None
        else:
            self.en_passant_square = square_to_idx(passant)
        self.draw_move_counter = draw
        self.move_counter = move_no

    def print_board(self):
        print("-" * 17)
        for rank in range(8):
            print("|", end="")
            for file in range(8):
                square = rank * 8 + file
                piece = self.chessboard[square]
                print(PIECE_TO_TEXT[piece] + "|", end="")
            print()
            print("-" * 17)
        if self.to_move == WHITE:
            print("White to move")
        elif self.to_move == BLACK:
            print("Black to move")
        if self.en_passant_square:
            print(
                f"En passant available on square {idx_to_square(self.en_passant_square)}"
            )
        print(f"Castling details: {self.castling_rights}")
        print(f"Number of moves with no development: {self.draw_move_counter}")
        print(f"Move number: {self.move_counter}")

    def gen_pieces(self):
        for i in range(64):
            piece = self.chessboard[i]
            self.pieces[piece].append(i)


c = ChessGameState()
c.print_board()
c.set_to_fen("rnbqkbnr/ppp3pp/8/3p1p2/3pPP1P/8/PPP3P1/RNBQKBNR w KQkq - 0 5")
c.print_board()
print(c.generate_pseudo_legal_moves_for(square_to_idx("h1")))
