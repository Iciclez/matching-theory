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
        algorithm = deferred_acceptance(json.load(f))
        a, b = algorithm.group_1_optimal(), algorithm.group_2_optimal()
        return a, b


def main():
    file_names = ['preferences_marriage.json',
                  'preferences_hospitals_doctors.json', 'preferences_schools_students.json']

    preferences_marriage_solution = (
        {'w1': ['m3'], 'w2': ['m1'], 'w3': ['m4'], 'w4': ['m2']},
        {'m1': ['w2'], 'm2': ['w4'], 'm3': ['w1'], 'm4': ['w3']}
    )

    preferences_hospitals_doctors_solution = (
        {'h1': ['d3', 'd4'], 'h2': ['d2'], 'h3': ['d1']},
        {'d1': ['h3'], 'd2': ['h2'], 'd3': ['h1'], 'd4': ['h1']}
    )

    preferences_schools_students_solution = (
        {'s1': ['i1'], 's2': ['i3', 'i4'], 's3': ['i2']},
        {'i1': ['s1'], 'i2': ['s3'], 'i3': ['s2'], 'i4': ['s2']}
    )

    solutions = [preferences_marriage_solution,
                 preferences_hospitals_doctors_solution, preferences_schools_students_solution]

    for x in range(len(file_names)):
        assert(solutions[x] == get_deferred_acceptance(file_names[x]))

    print('all tests passed')


main()
