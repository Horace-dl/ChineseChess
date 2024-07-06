class Machine:
    #  (if we need to assign value in here???)
    _alg_type = 0

    def __init__(self):
        _alg_type = 0  # "minmax"

    def set_algorithm_type(self, type):
        self._alg_type = type

    def get_algorithm_type(self):
        return self._alg_type

    def evaluation(self):
        pass

    def min_max(self):
        pass

    def alpha_beta(self):
        pass

