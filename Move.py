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