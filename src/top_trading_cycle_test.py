import top_trading_cycle

def main():

    file_names = ['preferences_marriage.json',
                  'preferences_hospitals_doctors.json', 'preferences_schools_students.json']

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

    solutions = [preferences_marriage_solution,
                 preferences_hospitals_doctors_solution, preferences_schools_students_solution]

    for x in range(len(file_names)):
        assert(solutions[x] == top_trading_cycle.get_top_trading_cycle(file_names[x]))

    print('all tests passed')


main()
