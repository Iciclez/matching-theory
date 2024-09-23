import collections
import copy
import json
import os
import unittest
from typing import Callable, Tuple

from src.matching_theory import deferred_acceptance, immediate_acceptance, top_trading_cycle


def get_test_files() -> dict[str, str]:
    directory_path = os.path.dirname(os.path.realpath(__file__))
    return {
        'preferences_marriage': f'{directory_path}/test_data/preferences_marriage.json',
        'preferences_hospitals_doctors': f'{directory_path}/test_data/preferences_hospitals_doctors.json',
        'preferences_schools_students': f'{directory_path}/test_data/preferences_schools_students.json'
    }


def read_test_file(file_name: str) -> Tuple[list[dict], dict]:
    with open(file_name) as f:
        preferences = json.load(f)
        group_names = ('group_1', 'group_2')
        groups = [dict(), dict()]
        capacities = collections.defaultdict(int)

        for entity in preferences[group_names[0]]:
            groups[0][entity['name']] = entity['preference']
            capacities[entity['name']] = entity['capacity']

        for entity in preferences[group_names[1]]:
            groups[1][entity['name']] = entity['preference']
            capacities[entity['name']] = entity['capacity']

        return groups, capacities


class TestAlgorithms(unittest.TestCase):

    def validate_expected(self, algorithm_name: str, algorithm: Callable, solutions: dict[str, Tuple[dict[str, list[str]], dict[str, list[str]]]]) -> Tuple[bool, str]:
        test_files = get_test_files()
        for key, solution in solutions.items():
            self.assertTrue(key in test_files.keys(), f'key "{
                            key}" not in test_files, test_files={test_files.keys()}')

            preferences, capacities = read_test_file(test_files[key])
            group_1_optimal_result = algorithm(copy.deepcopy(preferences[0]), copy.deepcopy(
                preferences[1]), copy.deepcopy(capacities), verbose=False)
            group_1_optimal_expected = solution[0]

            self.assertEqual(group_1_optimal_result, group_1_optimal_expected, f'{
                             algorithm_name}({key}) failed.')

            group_2_optimal_result = algorithm(copy.deepcopy(preferences[1]), copy.deepcopy(
                preferences[0]), copy.deepcopy(capacities), verbose=False)
            group_2_optimal_expected = solution[1]

            self.assertEqual(group_2_optimal_result, group_2_optimal_expected, f'{
                             algorithm_name}({key}) failed.')

    def test_deferred_acceptance(self):
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

        solutions = {'preferences_marriage': preferences_marriage_solution,
                     'preferences_hospitals_doctors': preferences_hospitals_doctors_solution,
                     'preferences_schools_students': preferences_schools_students_solution}

        self.validate_expected('deferred_acceptance',
                               deferred_acceptance, solutions)

    def test_immediate_acceptance(self):
        # ok
        preferences_marriage_solution = (
            {'w1': ['m1'], 'w2': ['m4'], 'w3': ['m3'], 'w4': ['m2']},
            {'m1': ['w4'], 'm2': ['w3'], 'm3': ['w1'], 'm4': ['w2']}
        )

        # ok
        preferences_hospitals_doctors_solution = (
            {'h1': ['d3', 'd4'], 'h2': ['d2'], 'h3': ['d1']},
            {'d1': ['h1'], 'd2': ['h1'], 'd3': ['h3'], 'd4': ['h2']}
        )

        preferences_schools_students_solution = (
            {'s1': ['i2'], 's2': ['i1', 'i4'], 's3': ['i3']},  # ok
            {'i1': ['s1'], 'i2': ['s3'], 'i3': ['s2'], 'i4': ['s2']}
        )

        solutions = {'preferences_marriage': preferences_marriage_solution,
                     'preferences_hospitals_doctors': preferences_hospitals_doctors_solution,
                     'preferences_schools_students': preferences_schools_students_solution}

        self.validate_expected('immediate_acceptance',
                               immediate_acceptance, solutions)

    def test_top_trading_cycle(self):
        preferences_marriage_solution = (
            {'m1': ['w1'], 'm2': ['w3'], 'm3': ['w4'], 'm4': ['w2']},
            {'w1': ['m3'], 'w2': ['m4'], 'w3': ['m2'], 'w4': ['m1']}
        )

        preferences_hospitals_doctors_solution = (
            {'d1': ['h3'], 'd2': ['h2'], 'd3': ['h1'], 'd4': ['h1']},
            {'h1': ['d1', 'd4'], 'h2': ['d2'], 'h3': ['d3']}
        )

        # ok
        preferences_schools_students_solution = (
            {'i1': ['s2'], 'i2': ['s3'], 'i3': ['s1'], 'i4': ['s2']},
            {'s1': ['i1'], 's2': ['i3', 'i4'], 's3': ['i2']}
        )

        solutions = {'preferences_marriage': preferences_marriage_solution,
                     'preferences_hospitals_doctors': preferences_hospitals_doctors_solution,
                     'preferences_schools_students': preferences_schools_students_solution}

        self.validate_expected('top_trading_cycle',
                               top_trading_cycle, solutions)


if __name__ == "__main__":
    unittest.main()
