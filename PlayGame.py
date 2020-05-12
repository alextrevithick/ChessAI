from ChessState import ChessState
import AlphaBeta
from ChessHeuristic import heur
import chess.pgn

if __name__ == '__main__':
    #Initializes an IntelligentPlayer with search depths 3 and 2
    player = AlphaBeta.IntelligentPlayer(heur, max_depth=3, quiescence_max_depth=2)

    color = ["black", "white"]

    print("This is a text-based chess interface, where the computer will play against the user or itself.")

    #Prompts user for game type
    type_of_game = None
    while True:
        type_of_game = input("In order of white versus black, where c means computer and h means human, type cvc, hvc, or cvh: ")
        if type_of_game in ["cvc", "cvh", "hvc"]:
            break

    #Prompts user for starting position
    while True:
        fen = input("Type 'n' for the standard starting position or a specific FEN: ")
        if fen is 'n':
            board = ChessState()
            break
        else:
            try:
                board = ChessState(fen=fen)
                break
            except ValueError:
                print("Invalid FEN")

    #Plays calculated best move in given position
    def play_engine_move():
        engine_move = board.san(player.best_move(board, board.turn))
        print("Computer move for " + color[board.turn] + " is " + engine_move)
        board.push_san(engine_move)

    #Prompts and plays user's move
    def prompt_and_play_user_move():
        while True:
            try:
                human_move = board.parse_san(input("Input move in SAN for " + color[board.turn] + ": "))
                break
            except ValueError:
                print("Invalid move, input again")
        board.push(human_move)

    #Loops over moves until game is over
    if (board.turn and type_of_game == 'cvh') or (not board.turn and type_of_game == 'hvc'):
        while not board.is_game_over():
            play_engine_move()
            prompt_and_play_user_move()
    elif (board.turn and type_of_game == 'hvc') or (not board.turn and type_of_game == 'cvh'):
        while not board.is_game_over():
            prompt_and_play_user_move()
            play_engine_move()
    elif type_of_game == 'cvc':
        while not board.is_game_over():
            play_engine_move()

    #prints the results of the game including PGN
    print()
    print("This is the PGN of the game:")
    game = chess.pgn.Game.from_board(board)
    print(game)


