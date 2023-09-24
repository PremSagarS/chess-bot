EMPTY = 0b00000
WHITE = 0b01000
BLACK = 0b10000
PAWN = 0b00001
KNIGHT = 0b00010
BISHOP = 0b00011
ROOK = 0b00100
QUEEN = 0b00101
KING = 0b00110

PIECE_TO_TEXT = {
    EMPTY: " ",
    BLACK | ROOK: "r",
    BLACK | KNIGHT: "n",
    BLACK | BISHOP: "b",
    BLACK | QUEEN: "q",
    BLACK | KING: "k",
    BLACK | PAWN: "p",
    WHITE | ROOK: "R",
    WHITE | KNIGHT: "N",
    WHITE | BISHOP: "B",
    WHITE | QUEEN: "Q",
    WHITE | KING: "K",
    WHITE | PAWN: "P",
}

TEXT_TO_PIECE = {v: k for k, v in PIECE_TO_TEXT.items()}

FILES_TO_IDX = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
RANKS_TO_IDX = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
IDX_TO_FILES = {v: k for k, v in FILES_TO_IDX.items()}
IDX_TO_RANKS = {v: k for k, v in RANKS_TO_IDX.items()}


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

    def square_to_idx(square):
        file = FILES_TO_IDX[square[0]]
        rank = RANKS_TO_IDX[square[1]]
        return rank * 8 + file

    def idx_to_square(idx):
        file_idx = idx % 8
        rank_idx = idx // 8
        return IDX_TO_FILES[file_idx] + IDX_TO_RANKS[rank_idx]

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
            self.en_passant_square = ChessGameState.square_to_idx(passant)
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
                f"En passant available on square {ChessGameState.idx_to_square(self.en_passant_square)}"
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
c.set_to_fen("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
c.print_board()
