from Move import Move
from typing import List


class State:
    """A skeleton state object"""
    def get_move_from_book(self) -> Move:
        pass

    def get_move_from_table(self) -> Move:
        pass

    def get_applicable_actions(self) -> List[Move]:
        pass

    def is_game_over(self, *, claim_draw: bool = True) -> bool:
        pass

    def has_won(self,maximizing_player) -> bool:
        pass

    def make_action_result(self, move: Move):
        pass

    def delete_action_result(self):
        pass

    def get_non_quiescent_actions(self) -> List[Move]:
        pass

