# chess-bot
Chess Bot

To-Do:

Move Class [x]

ChessGameState Class []
- [x] Data
- [x] set_to_fen(fen) => sets board state to fen and returns none
- [x] board_to_fen(void) => returns current board state as fen string
- [x] precomputemovedata(void) => computes the number of squares to edge in every direction for all squares
- [x] make_move
- [x] print_board(void) => void
- [x] display_board(fen string) => void
- [x] gen_pieces => Updates the current list of pieces and their indices
- [x] generate_pseudo_legal_moves_for => List of Move objects
- [x] generate_pseudo_legal_moves => List of move objects
- [x] legal_moves_for
- [ ] is_game_over
- [x] player_to_move
- [x] unmake_last_move
- [x] is_it_illegal() => true/false. returns true if you can capture opponent's king