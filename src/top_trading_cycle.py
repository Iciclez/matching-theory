from matching_algorithm import matching_algorithm
import json
import copy


class top_trading_cycle(matching_algorithm):
    def group_1_optimal(self):
        return self.match(copy.deepcopy(self.group_1), copy.deepcopy(self.group_2), 'top_trading_cycle', False)

    def group_2_optimal(self):
        return self.match(copy.deepcopy(self.group_2), copy.deepcopy(self.group_1), 'top_trading_cycle', False)


def get_top_trading_cycle(file_name):
    with open(file_name) as f:
        algorithm = top_trading_cycle(json.load(f), ('group_1', 'group_2'))
        a, b = algorithm.group_1_optimal(), algorithm.group_2_optimal()
        return a, b
