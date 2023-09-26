from random import randint


def randomZobristKey():
    return randint(0, pow(2, 64))


def generateZobristKeys():
    Table = [[randomZobristKey() for piece_idx in range(23)] for board_idx in range(64)]
    return Table


EMPTY = 0b00000
WHITE = 0b01000
BLACK = 0b10000
PAWN = 0b00001
KNIGHT = 0b00010
BISHOP = 0b00011
ROOK = 0b00100
QUEEN = 0b00101
KING = 0b00110

PROMOTETO_PIECES = [KNIGHT, BISHOP, ROOK, QUEEN]

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

DIRECTIONOFFSETS = [-8, 8, 1, -1, -7, -9, 9, 7]


def square_to_idx(square):
    file = FILES_TO_IDX[square[0]]
    rank = RANKS_TO_IDX[square[1]]
    return rank * 8 + file


def idx_to_square(idx):
    file_idx = idx % 8
    rank_idx = idx // 8
    return IDX_TO_FILES[file_idx] + IDX_TO_RANKS[rank_idx]


PAWN_MOVES_DIRECTION_OFFSET = {WHITE: -8, BLACK: 8}
PAWN_TAKES_DIRECTION_OFFSET = {WHITE: [5, 4], BLACK: [7, 6]}
PAWN_START_RANK = {WHITE: 6, BLACK: 1}
PAWN_PROMOTION_RANK = {WHITE: 0, BLACK: 7}

KINGSIDE_CASTLING = {WHITE: 0, BLACK: 2}
KINGSIDE_CASTLING_SQUARES = {WHITE: [61, 62], BLACK: [5, 6]}
KINGSIDE_CASTLING_ENDSQUARE = {WHITE: 62, BLACK: 6}
KINGSIDE_CASTLING_ROOK_ENDSQUARE = {WHITE: 61, BLACK: 5}
KINGSIDE_CASTLING_ROOKSQUARE = {WHITE: 63, BLACK: 7}
QUEENSIDE_CASTLING = {WHITE: 1, BLACK: 3}
QUEENSIDE_CASTLING_SQUARES = {WHITE: [57, 58, 59], BLACK: [1, 2, 3]}
QUEENSIDE_CASTLING_ENDSQUARE = {WHITE: 57, BLACK: 1}
QUEENSIDE_CASTLING_ROOK_ENDSQUARE = {WHITE: 59, BLACK: 3}
QUEENSIDE_CASTLING_ROOKSQUARE = {WHITE: 56, BLACK: 0}
NO_CASTLING = 4

KING_START_INDEX = {BLACK: 4, WHITE: 60}
