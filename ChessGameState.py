from Move import Move
from ChessConstants import *
from chessboard import display


class ChessGameState:
    def __init__(self):
        self.chessboard = [0] * 64
        self.draw_move_counter = 0
        self.drawMoveCounterOn = []
        self.move_counter = 1
        self.reachedPositions = dict()
        self.castling_rights = []
        self.castlingRightsOn = []
        self.en_passant_square = None
        self.enPassantSquareOn = []
        self.moves = []
        self.pieces = []
        self.set_to_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.numsquarestoedge = [[] for i in range(64)]
        self.precomputemovedata()
        self.zobristKeys = generateZobristKeys()

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

    def attacking_squares_of(self, start_square_idx):
        startSquarePiece = self.chessboard[start_square_idx]
        startSquarePieceType = startSquarePiece & 0b00111
        startSquarePieceColor = startSquarePiece & 0b11000

        attacking_squares = []

        if startSquarePieceType == KING:
            for directionIndex in range(8):
                if self.numsquarestoedge[start_square_idx][directionIndex] < 1:
                    continue
                end_square_idx = start_square_idx + DIRECTIONOFFSETS[directionIndex]
                endSquarePiece = self.chessboard[end_square_idx]
                endSquarePieceColor = endSquarePiece & 0b11000
                if endSquarePiece == EMPTY or endSquarePiece != startSquarePieceColor:
                    attacking_squares.append(end_square_idx)
            return attacking_squares

        if startSquarePieceType == KNIGHT:
            possibleOffsetValues = [(1, 2), (2, 1)]
            possibleOffsetSigns = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
            startRank = start_square_idx // 8
            startFile = start_square_idx % 8
            for offsetvalues in possibleOffsetValues:
                for offsetsigns in possibleOffsetSigns:
                    fileOffset = offsetvalues[0] * offsetsigns[0]
                    rankOffset = offsetvalues[1] * offsetsigns[1]
                    endRank = startRank + rankOffset
                    endFile = startFile + fileOffset
                    end_square_idx = endRank * 8 + endFile
                    if endRank < 0 or endRank > 7 or endFile < 0 or endFile > 7:
                        continue
                    endSquarePiece = self.chessboard[end_square_idx]
                    endSquarePieceColor = endSquarePiece & 0b11000
                    if (
                        endSquarePiece == EMPTY
                        or endSquarePieceColor != startSquarePiece
                    ):
                        attacking_squares.append(end_square_idx)
            return attacking_squares

        if startSquarePieceType == PAWN:
            for direction_idx in range(2):
                directionIndex = PAWN_TAKES_DIRECTION_OFFSET[startSquarePieceColor][
                    direction_idx
                ]
                if self.numsquarestoedge[start_square_idx][directionIndex] < 1:
                    continue
                end_square_idx = start_square_idx + DIRECTIONOFFSETS[directionIndex]
                endSquarePiece = self.chessboard[end_square_idx]
                endSquarePieceColor = endSquarePiece & 0b11000
                if (
                    endSquarePiece == EMPTY
                    or endSquarePieceColor != startSquarePieceColor
                ):
                    attacking_squares.append(end_square_idx)
            return attacking_squares

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
                endSquarePieceColor = endSquarePiece & 0b11000
                if endSquarePiece == EMPTY:
                    attacking_squares.append(end_square_idx)
                elif endSquarePieceColor != startSquarePieceColor:
                    attacking_squares.append(end_square_idx)
                    break
                else:
                    break

        return attacking_squares

    def is_in_check(self):
        kingSquare = self.pieces[self.to_move | KING][0]
        for pieceSquares in self.pieces:
            for square in pieceSquares:
                pieceOnSquare = self.chessboard[square]
                pieceOnSquareColor = pieceOnSquare & 0b11000
                if pieceOnSquare == EMPTY or pieceOnSquareColor == self.to_move:
                    continue
                attackingSquares = self.attacking_squares_of(square)
                if kingSquare in attackingSquares:
                    return True
        return False

    def generate_pseudo_legal_moves_for(self, start_square_idx):
        startSquarePiece = self.chessboard[start_square_idx]
        startSquarePieceType = startSquarePiece & 0b00111
        startSquarePieceColor = startSquarePiece & 0b11000
        if startSquarePieceColor != self.to_move or startSquarePiece == EMPTY:
            return []

        possibleMoves = []

        directionIndexStart = directionIndexEnd = None

        if startSquarePieceType == KNIGHT:
            possibleOffsetValues = [(1, 2), (2, 1)]
            possibleOffsetSigns = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
            startRank = start_square_idx // 8
            startFile = start_square_idx % 8
            for offsetvalues in possibleOffsetValues:
                for offsetsigns in possibleOffsetSigns:
                    fileOffset = offsetvalues[0] * offsetsigns[0]
                    rankOffset = offsetvalues[1] * offsetsigns[1]
                    endRank = startRank + rankOffset
                    endFile = startFile + fileOffset
                    end_square_idx = endRank * 8 + endFile
                    if endRank < 0 or endRank > 7 or endFile < 0 or endFile > 7:
                        continue
                    endSquarePiece = self.chessboard[end_square_idx]
                    endSquarePieceColor = endSquarePiece & 0b11000
                    if endSquarePiece == EMPTY or endSquarePieceColor != self.to_move:
                        possibleMoves.append(
                            Move(
                                start_square_idx,
                                end_square_idx,
                                startSquarePiece,
                                captured_piece=endSquarePiece,
                            )
                        )

            return possibleMoves

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
                    if end_square_idx // 8 == PAWN_PROMOTION_RANK[self.to_move]:
                        for piece in PROMOTETO_PIECES:
                            possibleMoves.append(
                                Move(
                                    start_square_idx,
                                    end_square_idx,
                                    startSquarePiece,
                                    self.to_move | piece,
                                    NO_CASTLING,
                                    endSquarePiece,
                                )
                            )
                    else:
                        possibleMoves.append(
                            Move(
                                start_square_idx,
                                end_square_idx,
                                startSquarePiece,
                                captured_piece=endSquarePiece,
                            )
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
                            Move(
                                start_square_idx,
                                end_square_idx,
                                startSquarePiece,
                                captured_piece=endSquarePiece,
                            )
                        )

            # Captures:
            for direction_idx in range(2):
                directionIndex = PAWN_TAKES_DIRECTION_OFFSET[self.to_move][
                    direction_idx
                ]
                if self.numsquarestoedge[start_square_idx][directionIndex] < 1:
                    continue
                end_square_idx = start_square_idx + DIRECTIONOFFSETS[directionIndex]
                endSquarePiece = self.chessboard[end_square_idx]
                endSquarePieceColor = endSquarePiece & 0b11000
                if (
                    endSquarePiece == EMPTY and self.en_passant_square == end_square_idx
                ) or (endSquarePiece != EMPTY and endSquarePieceColor != self.to_move):
                    if end_square_idx // 8 == PAWN_PROMOTION_RANK[self.to_move]:
                        for piece in PROMOTETO_PIECES:
                            possibleMoves.append(
                                Move(
                                    start_square_idx,
                                    end_square_idx,
                                    startSquarePiece,
                                    self.to_move | piece,
                                    NO_CASTLING,
                                    endSquarePiece,
                                )
                            )
                    else:
                        opponentColor = BLACK + WHITE - self.to_move
                        opponentPawn = opponentColor | PAWN
                        possibleMoves.append(
                            Move(
                                start_square_idx,
                                end_square_idx,
                                startSquarePiece,
                                captured_piece=opponentPawn
                                if endSquarePiece == EMPTY
                                else endSquarePiece,
                            )
                        )

            return possibleMoves

        if startSquarePieceType == KING:
            for directionidx in range(8):
                end_square_idx = start_square_idx + DIRECTIONOFFSETS[directionidx]
                if self.numsquarestoedge[start_square_idx][directionidx] < 1:
                    continue
                endSquarePiece = self.chessboard[end_square_idx]
                endSquarePieceColor = endSquarePiece & 0b11000

                if endSquarePiece == EMPTY or endSquarePieceColor != self.to_move:
                    possibleMoves.append(
                        Move(
                            start_square_idx,
                            end_square_idx,
                            startSquarePiece,
                            captured_piece=endSquarePiece,
                        )
                    )

                else:
                    continue

            # Castling:
            if start_square_idx == KING_START_INDEX[self.to_move]:
                if self.castling_rights[KINGSIDE_CASTLING[self.to_move]]:
                    castling_squares_empty = True
                    for square_idx in KINGSIDE_CASTLING_SQUARES[self.to_move]:
                        castling_squares_empty &= self.chessboard[square_idx] == EMPTY
                    if castling_squares_empty:
                        possibleMoves.append(
                            Move(
                                start_square_idx,
                                KINGSIDE_CASTLING_ENDSQUARE[self.to_move],
                                startSquarePiece,
                                None,
                                KINGSIDE_CASTLING[self.to_move],
                                endSquarePiece,
                            )
                        )

                if self.castling_rights[QUEENSIDE_CASTLING[self.to_move]]:
                    castling_squares_empty = True
                    for square_idx in QUEENSIDE_CASTLING_SQUARES[self.to_move]:
                        castling_squares_empty &= self.chessboard[square_idx] == EMPTY
                    if castling_squares_empty:
                        possibleMoves.append(
                            Move(
                                start_square_idx,
                                QUEENSIDE_CASTLING_ENDSQUARE[self.to_move],
                                startSquarePiece,
                                None,
                                QUEENSIDE_CASTLING[self.to_move],
                                endSquarePiece,
                            )
                        )

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
                        Move(
                            start_square_idx,
                            end_square_idx,
                            startSquarePiece,
                            captured_piece=endSquarePiece,
                        )
                    )
                elif endSquarePieceColor == self.to_move:
                    break
                else:
                    possibleMoves.append(
                        Move(
                            start_square_idx,
                            end_square_idx,
                            startSquarePiece,
                            captured_piece=endSquarePiece,
                        )
                    )
                    break
        return possibleMoves

    def generate_pseudo_legal_moves(self):
        possible_moves = []
        for square_indices in self.pieces[1:]:
            for square_index in square_indices:
                possible_moves.extend(
                    self.generate_pseudo_legal_moves_for(square_index)
                )
        return possible_moves

    def generate_legal_moves_for(self, square_idx):
        plmoves = self.generate_pseudo_legal_moves_for(square_idx)
        lmoves = []
        for plmove in plmoves:
            if plmove.castle == NO_CASTLING:
                self.make_move(plmove)
                if self.is_it_illegal() == False:
                    lmoves.append(plmove)
                self.unmake_last_move()
            else:
                movingPiece = plmove.piece
                movingPieceColor = movingPiece & 0b11000
                movingPieceType = movingPiece & 0b00111
                if plmove.castle == KINGSIDE_CASTLING[movingPieceColor]:
                    squares_to_check = (
                        [KING_START_INDEX[movingPieceColor]]
                        + KINGSIDE_CASTLING_SQUARES[movingPieceColor]
                        + [KINGSIDE_CASTLING_ENDSQUARE[movingPieceColor]]
                    )
                elif plmove.castle == QUEENSIDE_CASTLING[movingPieceColor]:
                    squares_to_check = (
                        [KING_START_INDEX[movingPieceColor]]
                        + KINGSIDE_CASTLING_SQUARES[movingPieceColor]
                        + [KINGSIDE_CASTLING_ENDSQUARE[movingPieceColor]]
                    )
                moveIsLegal = True
                self.make_move(plmove)
                new_plmoves = self.generate_pseudo_legal_moves()
                for new_plmove in new_plmoves:
                    if new_plmove.end_square in squares_to_check:
                        moveIsLegal = False
                        break
                if moveIsLegal:
                    lmoves.append(plmove)

        return lmoves

    def generate_legal_moves(self):
        possible_moves = []
        for square_indices in self.pieces[1:]:
            for square_index in square_indices:
                possible_moves.extend(self.generate_legal_moves_for(square_index))
        return possible_moves

    def make_enpassant_move(self, move):
        capturedRank = move.start_square // 8
        capturedFile = move.end_square % 8
        capturedSquare = capturedRank * 8 + capturedFile

        # update board
        self.chessboard[move.start_square] = EMPTY
        self.chessboard[move.end_square] = move.piece
        self.chessboard[capturedSquare] = EMPTY

        # update pieces
        self.pieces[move.piece].remove(move.start_square)
        self.pieces[EMPTY].append(move.start_square)
        self.pieces[move.piece].append(move.end_square)
        self.pieces[EMPTY].remove(move.end_square)
        self.pieces[EMPTY].append(capturedSquare)
        self.pieces[move.captured_piece].remove(capturedSquare)

        # update reachedPositions
        zobristHash = self.boardToZobristKey()
        self.reachedPositions[zobristHash] = (
            self.reachedPositions.get(zobristHash, 0) + 1
        )

        # no need to update castling rights
        self.castlingRightsOn.append(self.castling_rights)

        # update en passant square
        self.enPassantSquareOn.append(self.en_passant_square)
        self.en_passant_square = None

        # update draw move counter
        self.drawMoveCounterOn.append(self.draw_move_counter)
        self.draw_move_counter = 0

        # update move counter
        if move.piece & 0b11000 == BLACK:
            self.move_counter += 1

        # update moves
        self.moves.append(move)

    def unmake_enpassant_move(self, move):
        # updated move

        # update reachedPositions
        zobristHash = self.boardToZobristKey()
        self.reachedPositions[zobristHash] -= 1

        movingPiece = move.piece
        movingPieceColor = move.piece & 0b11000

        capturedRank = move.start_square // 8
        capturedFile = move.end_square % 8
        capturedSquare = capturedRank * 8 + capturedFile

        # update board
        self.chessboard[move.start_square] = move.piece
        self.chessboard[move.end_square] = EMPTY
        self.chessboard[capturedSquare] = move.captured_piece

        # update pieces
        self.pieces[move.piece].append(move.start_square)
        self.pieces[EMPTY].remove(move.start_square)
        self.pieces[move.piece].remove(move.end_square)
        self.pieces[EMPTY].append(move.end_square)
        self.pieces[EMPTY].remove(capturedSquare)
        self.pieces[move.captured_piece].append(capturedSquare)

        self.en_passant_square = self.enPassantSquareOn.pop()

        self.castling_rights = self.castlingRightsOn.pop()

        if movingPieceColor == BLACK:
            self.move_counter -= 1

        self.draw_move_counter = self.drawMoveCounterOn.pop()

    def make_castling_move(self, move):
        movingPiece = move.piece
        movingPieceColor = move.piece & 0b11000

        if move.castle == KINGSIDE_CASTLING[movingPieceColor]:
            rookStartSquare = KINGSIDE_CASTLING_ROOKSQUARE[movingPieceColor]
            rookEndSquare = KINGSIDE_CASTLING_ROOK_ENDSQUARE[movingPieceColor]

        elif move.castle == QUEENSIDE_CASTLING[movingPieceColor]:
            rookStartSquare = QUEENSIDE_CASTLING_ROOKSQUARE[movingPieceColor]
            rookEndSquare = QUEENSIDE_CASTLING_ROOK_ENDSQUARE[movingPieceColor]

        rookPiece = self.chessboard[rookStartSquare]

        # update board
        self.chessboard[move.start_square] = EMPTY
        self.chessboard[move.end_square] = movingPiece
        self.chessboard[rookStartSquare] = EMPTY
        self.chessboard[rookEndSquare] = rookPiece

        # update pieces
        self.pieces[movingPiece].remove(move.start_square)
        self.pieces[EMPTY].append(move.start_square)
        self.pieces[movingPiece].append(move.end_square)
        self.pieces[EMPTY].remove(move.end_square)

        self.pieces[rookPiece].remove(rookStartSquare)
        self.pieces[EMPTY].append(rookStartSquare)
        self.pieces[rookPiece].append(rookEndSquare)
        self.pieces[EMPTY].remove(rookEndSquare)

        # update reachedPositions
        zobristHash = self.boardToZobristKey()
        self.reachedPositions[zobristHash] = (
            self.reachedPositions.get(zobristHash, 0) + 1
        )

        # update castling rights
        self.castlingRightsOn.append([i for i in self.castling_rights])
        self.castling_rights[KINGSIDE_CASTLING[movingPieceColor]] = False
        self.castling_rights[QUEENSIDE_CASTLING[movingPieceColor]] = False

        # update en passant square
        self.enPassantSquareOn.append(self.en_passant_square)
        self.en_passant_square = None

        # update draw move counter
        self.drawMoveCounterOn.append(self.draw_move_counter)
        self.draw_move_counter = 0

        # update move counter
        if movingPieceColor == BLACK:
            self.move_counter += 1

        # update moves
        self.moves.append(move)

    def unmake_castling_move(self, move):
        # updated move

        # update reachedPositions
        zobristHash = self.boardToZobristKey()
        self.reachedPositions[zobristHash] -= 1

        movingPiece = move.piece
        movingPieceColor = move.piece & 0b11000
        if move.castle == KINGSIDE_CASTLING[movingPieceColor]:
            rookStartSquare = KINGSIDE_CASTLING_ROOKSQUARE[movingPieceColor]
            rookEndSquare = KINGSIDE_CASTLING_ROOK_ENDSQUARE[movingPieceColor]
        elif move.castle == QUEENSIDE_CASTLING[movingPieceColor]:
            rookStartSquare = QUEENSIDE_CASTLING_ROOKSQUARE[movingPieceColor]
            rookEndSquare = QUEENSIDE_CASTLING_ROOK_ENDSQUARE[movingPieceColor]
        rookPiece = self.chessboard[rookEndSquare]

        # update board
        self.chessboard[move.start_square] = movingPiece
        self.chessboard[move.end_square] = EMPTY
        self.chessboard[rookStartSquare] = rookPiece
        self.chessboard[rookEndSquare] = EMPTY

        # update pieces
        self.pieces[movingPiece].append(move.start_square)
        self.pieces[EMPTY].remove(move.start_square)
        self.pieces[movingPiece].remove(move.end_square)
        self.pieces[EMPTY].append(move.end_square)

        self.pieces[rookPiece].append(rookStartSquare)
        self.pieces[EMPTY].remove(rookStartSquare)
        self.pieces[rookPiece].remove(rookEndSquare)
        self.pieces[EMPTY].append(rookEndSquare)

        # update en passant square
        self.en_passant_square = self.enPassantSquareOn.pop()

        # update castling rights
        self.castling_rights = self.castlingRightsOn.pop()

        # update move counter
        if movingPieceColor == BLACK:
            self.move_counter -= 1

        # update draw move counter
        self.draw_move_counter = self.drawMoveCounterOn.pop()

    def make_promoting_move(self, move):
        # update board
        self.chessboard[move.start_square] = EMPTY
        self.chessboard[move.end_square] = move.promoteTo

        # update pieces
        self.pieces[move.piece].remove(move.start_square)
        self.pieces[EMPTY].append(move.start_square)
        self.pieces[move.promoteTo].append(move.end_square)
        self.pieces[EMPTY].remove(move.end_square)

        # update reachedPositions
        zobristHash = self.boardToZobristKey()
        self.reachedPositions[zobristHash] = (
            self.reachedPositions.get(zobristHash, 0) + 1
        )

        self.castlingRightsOn.append(self.castling_rights)

        self.enPassantSquareOn.append(self.en_passant_square)
        self.en_passant_square = None

        self.drawMoveCounterOn.append(self.draw_move_counter)
        self.draw_move_counter = 0

        if move.piece & 0b11000 == BLACK:
            self.move_counter += 1

        self.moves.append(move)

    def unmake_promoting_move(self, move):
        zobristHash = self.boardToZobristKey()
        self.reachedPositions[zobristHash] -= 1

        self.chessboard[move.start_square] = move.piece
        self.chessboard[move.end_square] = EMPTY

        self.pieces[move.piece].append(move.start_square)
        self.pieces[EMPTY].remove(move.start_square)
        self.pieces[move.promoteTo].remove(move.end_square)
        self.pieces[EMPTY].append(move.end_square)

        self.en_passant_square = self.enPassantSquareOn.pop()

        self.castling_rights = self.castlingRightsOn.pop()

        if move.piece & 0b11000 == BLACK:
            self.move_counter -= 1

        self.draw_move_counter = self.drawMoveCounterOn.pop()

    def make_move(self, move):
        self.to_move = BLACK + WHITE - self.to_move

        if move.castle != NO_CASTLING:
            self.make_castling_move(move=move)
            return

        if move.end_square == self.en_passant_square and move.piece & 0b00111 == PAWN:
            self.make_enpassant_move(move)
            return

        if move.promoteTo != EMPTY:
            self.make_promoting_move(move)
            return

        # update board
        self.chessboard[move.start_square] = EMPTY
        self.chessboard[move.end_square] = move.piece

        # update pieces
        self.pieces[move.captured_piece].remove(move.end_square)
        self.pieces[move.piece].remove(move.start_square)
        self.pieces[EMPTY].append(move.start_square)
        self.pieces[move.piece].append(move.end_square)

        # update reachedPositions
        zobristHash = self.boardToZobristKey()
        self.reachedPositions[zobristHash] = (
            self.reachedPositions.get(zobristHash, 0) + 1
        )

        # update castling rights
        self.castlingRightsOn.append([i for i in self.castling_rights])
        if self.castling_rights[KINGSIDE_CASTLING[BLACK]]:
            if move.start_square == 7 or move.end_square == 7:
                self.castling_rights[KINGSIDE_CASTLING[BLACK]] = False

        if self.castling_rights[KINGSIDE_CASTLING[WHITE]]:
            if move.start_square == 63 or move.end_square == 63:
                self.castling_rights[KINGSIDE_CASTLING[WHITE]] = False

        if self.castling_rights[QUEENSIDE_CASTLING[BLACK]]:
            if move.start_square == 0 or move.end_square == 0:
                self.castling_rights[QUEENSIDE_CASTLING[BLACK]] = False

        if self.castling_rights[QUEENSIDE_CASTLING[WHITE]]:
            if move.start_square == 56 or move.end_square == 56:
                self.castling_rights[QUEENSIDE_CASTLING[WHITE]] = False

        # update en passant square
        self.enPassantSquareOn.append(self.en_passant_square)
        if move.piece & 0b00111 == PAWN:
            startSquareRank = move.start_square // 8
            endSquareRank = move.end_square // 8
            if abs(startSquareRank - endSquareRank) == 2:
                enPassantFile = move.start_square % 8
                enPassantRank = (startSquareRank + endSquareRank) // 2
                enPassantSquare = enPassantRank * 8 + enPassantFile
                self.en_passant_square = enPassantSquare
            else:
                self.en_passant_square = None
        else:
            self.en_passant_square = None

        # update draw move counter
        self.drawMoveCounterOn.append(self.draw_move_counter)
        if move.piece & 0b00111 != PAWN and move.captured_piece == EMPTY:
            self.draw_move_counter += 1
        else:
            self.draw_move_counter = 0

        # update move counter
        if move.piece & 0b11000 == BLACK:
            self.move_counter += 1

        # update moves
        self.moves.append(move)

    def unmake_last_move(self):
        self.to_move = BLACK + WHITE - self.to_move

        # update moves
        move = self.moves.pop()

        if move.castle != NO_CASTLING:
            self.unmake_castling_move(move)
            return

        if (
            move.end_square == self.enPassantSquareOn[-1]
            and move.piece & 0b00111 == PAWN
        ):
            self.unmake_enpassant_move(move)
            return

        if move.promoteTo != EMPTY:
            self.unmake_promoting_move(move)
            return

        # update reahchedPositions
        zobristHash = self.boardToZobristKey()
        self.reachedPositions[zobristHash] -= 1

        # update board
        self.chessboard[move.start_square] = move.piece
        self.chessboard[move.end_square] = move.captured_piece

        # update pieces
        self.pieces[move.captured_piece].append(move.end_square)
        self.pieces[move.piece].append(move.start_square)
        self.pieces[move.piece].remove(move.end_square)
        self.pieces[EMPTY].remove(move.start_square)

        # update en passant square
        self.en_passant_square = self.enPassantSquareOn.pop()

        # update casling rights
        self.castling_rights = self.castlingRightsOn.pop()

        # update move counter
        if move.piece & 0b11000 == BLACK:
            self.move_counter -= 1

        # update draw move counter
        self.draw_move_counter = self.drawMoveCounterOn.pop()

    def is_it_illegal(self):
        plmoves = self.generate_pseudo_legal_moves()
        for plmove in plmoves:
            if plmove.captured_piece & 0b00111 == KING:
                return True

        return False

    def boardToZobristKey(self):
        h = 0
        for board_idx in range(63):
            piece = self.chessboard[board_idx]
            if piece != EMPTY:
                h ^= self.zobristKeys[board_idx][piece]
        return h

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
        self.draw_move_counter = int(draw)
        self.move_counter = int(move_no)
        self.gen_pieces()

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
        if op[-1] == "/":
            op += "8"
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
        self.pieces = [[] for i in range(23)]
        for i in range(64):
            piece = self.chessboard[i]
            self.pieces[piece].append(i)

    def is_checkmate(self):
        # Implement legal_moves and check if any move is available
        if not self.is_in_check():
            return False
        kingSquare = self.pieces[self.to_move | KING][0]
        if len(self.generate_legal_moves()) != 0:
            return False
        return True


c = ChessGameState()
c.set_to_fen("1r6/8/r3k3/8/8/K7/8/8 w - - 0 3")
print(c.generate_legal_moves())
print(c.is_in_check())
print(c.is_checkmate())
print(c.board_to_fen())
