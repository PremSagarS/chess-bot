class ChessGameState:
    def __init__(self):
        self.chessboard = [0b1100,0b1010,0b1011,0b1101,0b1110,0b1011,0b1010,0b1100] + [0b1001] * 8 + [0b0000] * 32 + [0b0001] * 8 + [0b0100,0b0010,0b0011,0b0101,0b0110,0b0011,0b0010,0b0100]
        self.move_timer = 0.0
        self.fen_notation = ""
        self.castling_rights = [False, False, False, False]
        self.en_passant_square = None
        self.moves = []
        self.pieces = [None]*32