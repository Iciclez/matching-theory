from matching_algorithm import matching_algorithm
import json
import copy


class deferred_acceptance(matching_algorithm):
    def group_1_optimal(self):
        return self.match(copy.deepcopy(self.group_1), copy.deepcopy(self.group_2), 'deferred', False)

    def group_2_optimal(self):
        return self.match(copy.deepcopy(self.group_2), copy.deepcopy(self.group_1), 'deferred', False)


def get_deferred_acceptance(file_name):
    with open(file_name) as f:
        algorithm = deferred_acceptance(json.load(f), ('group_1', 'group_2'))
        a, b = algorithm.group_1_optimal(), algorithm.group_2_optimal()
        return a, b
