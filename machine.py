from ai_engine import alpha_beta


class Machine:
    _alg_type = 0

    def __init__(self):
        self._alg_type = 0

    def set_algorithm_type(self, type):
        self._alg_type = type

    def get_algorithm_type(self):
        return self._alg_type

    def evaluation(self):
        # placeholder: evaluation is implemented in `ai_engine.evaluate`
        pass

    def min_max(self):
        # not implemented; prefer alpha-beta
        pass

    def alpha_beta(self, rule_mgr, depth=3, maximizing_player=True):
        """Run alpha-beta search and return (score, move).

        `rule_mgr` should be an instance of `RuleMgr` with `_piece_list` populated.
        """
        return alpha_beta(rule_mgr, depth, maximizing_player)

