from Move import Move
from ChessConstants import *
from chessboard import display


class ChessGameState:
    def __init__(self):
        self.chessboard = [0] * 64
        self.draw_move_counter = 0
        self.move_counter = 1
        self.fen_notations = []
        self.castling_rights = []
        self.en_passant_square = None
        self.moves = []
        self.pieces = [[] for i in range(23)]
        self.set_to_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.gen_pieces()
        self.numsquarestoedge = [[] for i in range(64)]
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

        if startSquarePieceType == PAWN:
            # Normal forward pushes
            for moveRange in range(1, 3):
                end_square_idx = (
                    start_square_idx
                    + PAWN_MOVES_DIRECTION_OFFSET[self.to_move] * moveRange
                )
                if end_square_idx < 0 or end_square_idx > 63:
                    continue
                endSquarePiece = self.chessboard[end_square_idx]
                if endSquarePiece == EMPTY and moveRange == 1:
                    possibleMoves.append(
                        Move(start_square_idx, end_square_idx, startSquarePiece)
                    )
                elif (
                    moveRange == 2
                    and endSquarePiece == EMPTY
                    and start_square_idx // 8 == PAWN_START_RANK[self.to_move]
                ):
                    moveOnceEndSquareIndex = (
                        start_square_idx + PAWN_MOVES_DIRECTION_OFFSET[self.to_move]
                    )
                    moveOnceEndSquarePiece = self.chessboard[moveOnceEndSquareIndex]
                    if moveOnceEndSquarePiece == EMPTY:
                        possibleMoves.append(
                            Move(start_square_idx, end_square_idx, startSquarePiece)
                        )

            # Captures:
            for direction_idx in range(2):
                end_square_idx = (
                    start_square_idx
                    + PAWN_TAKES_DIRECTION_OFFSET[self.to_move][direction_idx]
                )
                endSquarePiece = self.chessboard[end_square_idx]
                endSquarePieceColor = endSquarePiece & 0b11000
                if (
                    endSquarePiece == EMPTY and self.en_passant_square == end_square_idx
                ) or (endSquarePiece != EMPTY and endSquarePieceColor != self.to_move):
                    possibleMoves.append(
                        Move(start_square_idx, end_square_idx, startSquarePiece)
                    )

            return possibleMoves

        if startSquarePieceType == KING:
            for directionidx in range(8):
                end_square_idx = start_square_idx + DIRECTIONOFFSETS[directionidx]
                if end_square_idx < 0 or end_square_idx > 63:
                    continue
                endSquarePiece = self.chessboard[end_square_idx]
                endSquarePieceColor = endSquarePiece & 0b11000

                if endSquarePiece == EMPTY or endSquarePieceColor != self.to_move:
                    possibleMoves.append(
                        Move(start_square_idx, end_square_idx, startSquarePiece)
                    )

                else:
                    continue

            return possibleMoves

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
                endSquarePieceColor = endSquarePiece & 0b11000
                if endSquarePiece == EMPTY:
                    possibleMoves.append(
                        Move(start_square_idx, end_square_idx, startSquarePiece)
                    )
                elif endSquarePieceColor == self.to_move:
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

    def board_to_fen(self):
        op = ""
        buffer = 0
        for i in range(64):
            cur = self.chessboard[i]
            if cur == 0:
                buffer += 1
            else:
                if buffer != 0:
                    op += str(buffer)
                    buffer = 0
                op += PIECE_TO_TEXT[cur]
            if (i + 1) % 8 == 0 and i != 63:
                if buffer != 0:
                    op += str(buffer)
                    buffer = 0
                op += "/"
        if self.to_move == WHITE:
            op += " w"
        else:
            op += " b"
        op += " "
        casrightsalpha = ["K", "Q", "k", "q"]
        if self.castling_rights == [False] * 4:
            op += "-"
        else:
            for i in range(4):
                if self.castling_rights[i]:
                    op += casrightsalpha[i]
        if self.en_passant_square == None:
            op += " -"
        else:
            op += " " + idx_to_square(self.en_passant_square)
        op += " " + str(self.draw_move_counter)
        op += " " + str(self.move_counter)
        return op

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

    def display_board(self, fen):
        game_board = display.start()
        while True:
            display.check_for_quit()
            display.update(fen, game_board)

    def gen_pieces(self):
        for i in range(64):
            piece = self.chessboard[i]
            self.pieces[piece].append(i)


c = ChessGameState()
c.print_board()
c.set_to_fen("rnbqkbnr/p1pp1ppp/4p3/1p1P4/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 3")
c.display_board(c.board_to_fen())
print(c.board_to_fen())
