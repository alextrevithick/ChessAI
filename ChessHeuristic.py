import chess
from ChessState import ChessState

#tables representing the values of having pieces in the given squares
#first row is the first from the player's perspective
pawntable = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
 0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

#values of king position in middlegame
kingstable_middlegame = [
 20, 30, 10,  0,  0, 10, 30, 20,
 20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]

#values of king position in endgame
kingstable_endgame = [
-50,-30,-30,-30,-30,-30,-30,-50,
-30,-30,  0,  0,  0,  0,-30,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-20,-10,  0,  0,-10,-20,-30,
-50,-40,-30,-20,-20,-30,-40,-50]

def heur(board: ChessState) -> int:
    """Evaluation function for a given ChessState. The upper- and lower-bounds for the value returned are
    10000 and -10000. A value of 0 indicates an equal position."""

    if board.is_checkmate():
        if board.turn:
            #black won
            return -10000
        else:
            #white won
            return 10000
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0

    #get piece positions
    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    black_pawns = board.pieces(chess.PAWN, chess.BLACK)
    white_knights = board.pieces(chess.KNIGHT, chess.WHITE)
    black_knights = board.pieces(chess.KNIGHT, chess.BLACK)
    white_bishops = board.pieces(chess.BISHOP, chess.WHITE)
    black_bishops = board.pieces(chess.BISHOP, chess.BLACK)
    white_rooks = board.pieces(chess.ROOK, chess.WHITE)
    black_rooks = board.pieces(chess.ROOK, chess.BLACK)
    white_queens = board.pieces(chess.QUEEN, chess.WHITE)
    black_queens = board.pieces(chess.QUEEN, chess.BLACK)
    white_king = board.pieces(chess.KING, chess.WHITE)
    black_king = board.pieces(chess.KING, chess.BLACK)

    num_of_pieces = len(black_knights) + len(black_bishops) + len(black_rooks) +\
                    len(white_knights) + len(white_bishops) + len(white_rooks) + len(white_queens) \
                    + len(black_queens) + len(white_king) + len(black_king) + len(white_pawns) + len(black_pawns)

    #returns number of pinned pieces from piece_set * value_of_pin
    def pinned_eval(piece_set, color, value_of_pin):
        cum_eval = 0
        for piece in piece_set:
            if board.is_pinned(color, piece):
                cum_eval = cum_eval + value_of_pin
        return cum_eval

    pinned_value = pinned_eval(white_pawns, chess.WHITE, -20) + pinned_eval(black_pawns, chess.BLACK, 20) + \
                         pinned_eval(white_knights, chess.WHITE, -30) + pinned_eval(black_knights, chess.BLACK, 30) +\
                         pinned_eval(white_bishops,chess.WHITE, -30) + pinned_eval(black_bishops,chess.BLACK, 30) +\
                         pinned_eval(white_rooks,chess.WHITE, -150) + pinned_eval(black_bishops,chess.BLACK, 150) +\
                         pinned_eval(white_queens,chess.WHITE, -400) + pinned_eval(black_bishops,chess.BLACK, 400)

    #returns value representing how many pieces of any type in list_of_pieces_to_attack are being attacked by any piece in piece_set
    def attacking_eval(piece_set, list_of_pieces_to_attack, list_of_value_of_attack):
        cum_eval = 0
        for piece in piece_set:
            attacked = board.attacks(piece)
            for i in range(0,len(list_of_pieces_to_attack)):
                num_of_attacks_on_piece_type = len(attacked.intersection(list_of_pieces_to_attack[i]))
                cum_eval = cum_eval + num_of_attacks_on_piece_type * list_of_value_of_attack[i]
        return cum_eval

    attacking_value = attacking_eval(white_knights, [black_queens,black_rooks,black_bishops], [20, 10, 5]) + \
      attacking_eval(white_bishops, [black_queens, black_rooks, black_bishops], [20, 10, 2]) + \
      attacking_eval(white_pawns, [black_queens, black_rooks, black_bishops, black_knights], [30, 20, 10, 10]) +\
      attacking_eval(white_rooks, [black_queens], [20]) + \
      attacking_eval(black_knights, [white_queens, white_rooks, white_bishops], [-20, -10, -5]) + \
      attacking_eval(black_bishops, [white_queens, white_rooks, white_bishops], [-20, -10, -2]) + \
      attacking_eval(black_pawns, [white_queens, white_rooks, white_bishops, white_knights], [-30, -20, -10, -10]) + \
      attacking_eval(black_rooks, [white_queens], [-20])

    num_black_minor_pieces = len(black_knights) + len(black_bishops) + len(black_rooks)
    num_white_minor_pieces = len(white_knights) + len(white_bishops) + len(white_rooks)

    #boolean if board is in endgame
    endgame = (len(white_queens) + len(black_queens) is 0) or (len(white_queens) is 1 and len(black_queens) is 1 and
                                                   num_black_minor_pieces is 1 and num_white_minor_pieces is 1)

    kingstable = kingstable_endgame if endgame else kingstable_middlegame

    #bishop pair is more valuable
    white_value_of_bishops = 375 if len(white_bishops) >= 2 and len(black_bishops) < 2 else 360
    black_value_of_bishops = 375 if len(black_bishops) >= 2 and len(white_bishops) < 2 else 360

    #calculates value of material in centipawns with standard valuations from https://en.wikipedia.org/wiki/Chess_piece_relative_value
    white_material = 100 * len(white_pawns) + 350 * len(white_knights) + white_value_of_bishops * len(white_bishops) + 525 * len(white_rooks) + 900 * len(white_queens)
    black_material = 100 * len(black_pawns) + 350 * len(black_knights) + black_value_of_bishops * len(black_bishops) + 525 * len(black_rooks) + 900 * len(black_queens)

    #sums values of all the positions of the pieces on the board from the tables
    square_values = sum([pawntable[i] for i in white_pawns]) - sum([pawntable[chess.square_mirror(i)] for i in black_pawns]) +\
                    sum([knightstable[i] for i in white_knights]) - sum([knightstable[chess.square_mirror(i)] for i in black_knights]) +\
                    sum([bishopstable[i] for i in white_bishops]) - sum([bishopstable[chess.square_mirror(i)] for i in black_bishops])+\
                    sum([rookstable[i] for i in white_rooks]) - sum([rookstable[chess.square_mirror(i)] for i in black_rooks])+\
                    sum([queenstable[i] for i in white_queens]) - sum([queenstable[chess.square_mirror(i)] for i in black_queens])+\
                    sum([kingstable[i] for i in white_king]) - sum([kingstable[chess.square_mirror(i)] for i in black_king])

    return white_material - black_material + square_values + pinned_value + attacking_value
