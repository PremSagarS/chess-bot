import unittest
from ChessGameState import ChessGameState


def perft(depth: int, cgs: ChessGameState):
    if depth == 0:
        return 1

    nodes = 0

    moves = cgs.generate_pseudo_legal_moves()
    for move in moves:
        cgs.make_move(move)
        if not cgs.is_it_illegal():
            nodes += perft(depth - 1, cgs)
        cgs.unmake_last_move()

    return nodes


class TestPerft(unittest.TestCase):
    def test_init(self):
        cgs = ChessGameState()
        cgs.set_to_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        results = [1, 20, 400, 8902, 197281]
        for i in range(5):
            self.assertEqual(perft(i, cgs), results[i])

    def test_pos2(self):
        cgs = ChessGameState()
        cgs.set_to_fen(
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        )
        results = [1, 48, 2039, 97862]
        for i in range(4):
            self.assertEqual(perft(i, cgs), results[i])

    def test_pos3(self):
        cgs = ChessGameState()
        cgs.set_to_fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1")
        results = [1, 14, 191, 2812, 43238]
        for i in range(5):
            self.assertEqual(perft(i, cgs), results[i])

    def test_pos4(self):
        cgs = ChessGameState()
        cgs.set_to_fen(
            "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
        )
        results = [1, 6, 264, 9467, 422333]
        for i in range(5):
            self.assertEqual(perft(i, cgs), results[i])

    def test_pos5(self):
        cgs = ChessGameState()
        cgs.set_to_fen("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
        results = [1, 44, 1486, 62379]
        for i in range(4):
            self.assertEqual(perft(i, cgs), results[i])

    def test_pos6(self):
        cgs = ChessGameState()
        cgs.set_to_fen(
            "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"
        )
        results = [1, 46, 2079, 89890]
        for i in range(4):
            self.assertEqual(perft(i, cgs), results[i])


if __name__ == "__main__":
    unittest.main()
