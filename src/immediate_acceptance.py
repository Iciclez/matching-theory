from matching_algorithm import matching_algorithm
import json
import copy


class immediate_acceptance(matching_algorithm):
    def group_1_optimal(self):
        return self.match(copy.deepcopy(self.group_1), copy.deepcopy(self.group_2), 'immediate', False)

    def group_2_optimal(self):
        return self.match(copy.deepcopy(self.group_2), copy.deepcopy(self.group_1), 'immediate', False)


def get_immediate_acceptance(file_name):
    with open(file_name) as f:
        algorithm = immediate_acceptance(json.load(f))
        a, b = algorithm.group_1_optimal(), algorithm.group_2_optimal()
        return a, b
