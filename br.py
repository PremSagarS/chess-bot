class ChessGameState:
    def __init__(self):
        self.chessboard = [0]*64
        self.move_timer = 0.0
        self.fen_notation = ""
        self.castling_rights = [False, False, False, False]
        self.en_passant_square = None
        self.moves = []
        self.pieces = [None]*32

