from chess import Board
import chess.polyglot
import chess.syzygy
from State import State
from Move import Move
from typing import List

class ChessState(Board, State):
    """A state implementation for chess boards"""

    def __init__(self, *args, **kwargs):
        #same constructor, just added fields for opening book and table base
        Board.__init__(self, *args, **kwargs)
        # table of values for endgames of 3,4, and 5 pieces, showing how many moves until mate, or if position is drawn
        self.end_tablebase = chess.syzygy.open_tablebase("3-4-5")
        # here you can add directorys to the table base for more pieces (6 and 7), which takes many terrabytes
        self.end_tablebase_num_of_pieces = [3, 4, 5]
        # book of opening positions from which to play, if position has been encountered
        self.opening_memory_map = chess.polyglot.MemoryMappedReader("ProDeo.bin")


    def get_move_from_book(self) -> Move:
        '''Fetches book move if it exists, and returns None otherwise.'''
        try:
            return self.opening_memory_map.choice(self).move
        #position not found
        except IndexError:
            return None

    def get_move_from_table(self) -> Move:
        '''If position has been encountered in endgame table, finds best move if in a winning or drawn position. If not,
        if there is a capture which leads to a winning position, then this capture move is returned. If neither, None.'''

        num_of_pieces = sum([self.piece_at(i) is not None for i in range(0,64)])

        if num_of_pieces in self.end_tablebase_num_of_pieces:
            #now tablebase knows all positions reachable from current position (all have <=5 pieces)
            depth_to_win_or_loss = self.end_tablebase.get_dtz(self)
            for move in super().legal_moves:
                best_is_draw = depth_to_win_or_loss is 0
                self.make_action_result(move)
                #need to multiply by -1 because after action result, board.turn has been negated
                child_depth_to_win_or_loss = -1 * self.end_tablebase.get_dtz(self)
                #this conditional statement depends entirely on the implementation of get_dtz from chess.syzygy.open_tablebase
                #the first disjunct: if this value is 0, then the position is drawn, so the best moves are those that preserve the draw
                #the second disjunct: if this value is positive, then we are winning, and we must pick a move which
                #makes the value less positive, but not zero, so that we are closer to mate
                #the third disjunct: if this value is negative, then we are losing, so we make it as hard to mate as
                #possible by choosing half-moves which are only one closer to mate
                if (best_is_draw and child_depth_to_win_or_loss == 0) or \
                        (child_depth_to_win_or_loss < depth_to_win_or_loss and depth_to_win_or_loss > 0 and child_depth_to_win_or_loss > 0) or \
                        (depth_to_win_or_loss<0 and child_depth_to_win_or_loss == depth_to_win_or_loss + 1):
                    self.delete_action_result()
                    return move
                #if depth is 1, then position is won in one move
                elif depth_to_win_or_loss is 1:
                    #check if color who played last turn has won
                    if self.has_won(not self.turn):
                        self.delete_action_result()
                        return move
                self.delete_action_result()
        else:
            #checks if we can simplify to get to a winning position by making a capture
            #endgame table can evaluate some positions with more than 5 pieces
            for action in [x for x in super().legal_moves if self.is_capture(x)]:
                self.make_action_result(action)
                eval = self.end_tablebase.get_dtz(self)
                if eval is not None and eval < 0:
                    self.delete_action_result()
                    return action
                self.delete_action_result()
        return None

    def is_move_a_check(self, move) -> bool:
        super().push(move)
        is_move_a_check = self.is_check()
        super().pop()
        return is_move_a_check

    def is_move_go_out_of_check(self, move) -> bool:
        return self.is_check() and self.is_legal(move)

    def get_applicable_actions(self) -> List[Move]:
        return super().legal_moves

    #this method is in both super classes, so we inherit from Board
    def is_game_over(self) -> bool:
        return super().is_game_over(claim_draw = True)

    def has_won(self, color: bool) -> bool:
        return self.turn is not color and self.is_checkmate()

    def make_action_result(self, move):
        super().push(move)

    def delete_action_result(self):
        super().pop()

    def get_non_quiescent_actions(self) -> List[Move]:
        # we arbitrarily define non-quiescent actions as captures, moves into and out of check and promotions
        return [x for x in super().legal_moves if self.is_capture(x) or self.is_move_a_check(x) or self.is_move_go_out_of_check(x)
                or x.promotion is chess.QUEEN or x.promotion is chess.KNIGHT]

