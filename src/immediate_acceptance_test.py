import immediate_acceptance

def main():
    file_names = ['preferences_marriage.json',
                  'preferences_hospitals_doctors.json', 'preferences_schools_students.json']

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

    solutions = [preferences_marriage_solution,
                 preferences_hospitals_doctors_solution, preferences_schools_students_solution]

    for x in range(len(file_names)):
        assert(solutions[x] == immediate_acceptance.get_immediate_acceptance(file_names[x]))

    print('all tests passed')


main()
