import typing
from State import State
from Move import Move



class IntelligentPlayer:
    """An intelligent player that plays moves in two player games based on a given heuristic"""
    #note that a depth of -1 indicates that search will continue until terminal state or quiet
    def __init__(self, heuristic: typing.Callable[[State], int], max_depth: int = -1, quiescence_max_depth: int = -1):
        self.heuristic = heuristic
        self.max_depth = max_depth
        self.count = 0
        self.quiescence_max_depth = quiescence_max_depth

    # minimax implementation
    def minimax_solve(self, current_state: State, depth: int, max_node: bool) -> int:
        self.count = self.count + 1

        if current_state.is_game_over() or depth is self.max_depth:
            return self.heuristic(current_state)

        elif max_node:
            best_val = -100000
            actions = current_state.get_applicable_actions()
            for action in actions:
                current_state.make_action_result(action)  # now its the child of the state above
                value = self.minimax_solve(current_state, depth + 1, False)
                current_state.delete_action_result()  # now its the same as the above parameter passed again
                best_val = max(best_val, value)
            return best_val

        else:
            best_val = 100000
            actions = current_state.get_applicable_actions()
            for action in actions:
                current_state.make_action_result(action)  # now its the child of the state above
                value = self.minimax_solve(current_state, depth + 1, True)
                current_state.delete_action_result() # now its the same as the above parameter passed again
                best_val = min(best_val, value)
            return best_val

    #implements fail-soft alpha-beta pruning as in Oxford notes for AI
    def alpha_beta_solve(self, current_state: State, depth: int, max_node: bool, alpha: int, beta: int) -> int:
        self.count = self.count + 1
        if current_state.is_game_over():
            return self.heuristic(current_state)
        elif depth is self.max_depth:
            #node is still max or min
            return self.quiescence_search(current_state, 0, max_node, alpha, beta)

        elif max_node:
            best_val = -100000
            actions = current_state.get_applicable_actions()
            for action in actions:
                current_state.make_action_result(action)  # now its the child of the state above
                value = self.alpha_beta_solve(current_state, depth + 1, False, alpha, beta)
                current_state.delete_action_result()  # now its the same as the above parameter passed again
                best_val = max(best_val, value)
                if best_val >= beta:
                    #current evaluation bigger than beta so opponent wouldn't allow this position
                    return best_val
                alpha = max(best_val, alpha)
            return best_val

        else:
            best_val = 100000
            actions = current_state.get_applicable_actions()
            for action in actions:
                current_state.make_action_result(action)  # now its the child of the state above
                value = self.alpha_beta_solve(current_state, depth + 1, True, alpha, beta)
                current_state.delete_action_result() # now its the same as the above parameter passed again
                best_val = min(best_val, value)
                if best_val <= alpha:
                    return best_val
                beta = min(best_val, beta)
            return best_val

    #fail-soft implementation of a quiescence search
    def quiescence_search(self, current_state: State, depth: int, max_node: bool, alpha: int, beta: int) -> int:
        if current_state.is_game_over() or depth is self.quiescence_max_depth:
            return self.heuristic(current_state)
        non_quiescent_actions = current_state.get_non_quiescent_actions()
        if not non_quiescent_actions:
            # There are no non-quiescent actions available, so we are in a quiet state
            return self.heuristic(current_state)

        elif max_node:
            best_val = -100000
            stand_pat = self.heuristic(current_state)
            if stand_pat >= beta:
                return stand_pat
            if alpha < stand_pat:
                alpha = stand_pat

            for action in non_quiescent_actions:
                current_state.make_action_result(action)  # now its the child of the state above
                value = self.quiescence_search(current_state, depth + 1, False, alpha, beta)
                current_state.delete_action_result()  # now its the same as the above parameter passed again
                best_val = max(best_val, value)
                if best_val >= beta:
                    return best_val
                alpha = max(best_val, alpha)
            return best_val

        else:
            stand_pat = self.heuristic(current_state)
            if stand_pat <= alpha:
                return stand_pat
            if stand_pat < beta:
                beta = stand_pat

            best_val = 100000
            for action in non_quiescent_actions:
                current_state.make_action_result(action)  # now its the child of the state above
                value = self.quiescence_search(current_state, depth + 1, True, alpha, beta)
                current_state.delete_action_result() # now its the same as the above parameter passed again
                best_val = min(best_val, value)
                if best_val <= alpha:
                    return best_val
                beta = min(best_val, beta)
            return best_val

    #returns best move in given position
    def best_move(self, current_state: State, maximizing_player: bool) -> Move:
        self.count = 0

        #searches book for best move
        best_action = current_state.get_move_from_book()
        if best_action is not None:
            return best_action

        #searches table for best move
        best_action = current_state.get_move_from_table()
        if best_action is not None:
            return best_action

        if maximizing_player:
            def func(x, y):
                return x > y
        else:
            def func(x, y):
                return x < y

        actions = current_state.get_applicable_actions()
        assert (actions is not None)

        best_value = -1000000 if maximizing_player else 1000000

        for action in actions:
            current_state.make_action_result(action)
            action_value = self.alpha_beta_solve(current_state, 1, not maximizing_player, -10000000, 10000000)
            #for plain minimax search: action_value = self.minimax_solve(current_state, 1, not maximizing_player)
            current_state.delete_action_result()
            if func(action_value, best_value):
                best_value = action_value
                best_action = action
        return best_action
