from itertools import pairwise

input_file = r'input.txt'

safe_reports = 0
with open(input_file) as file:
    reports_as_chars = (line.split() for line in file)
    reports = ([int(x) for x in rep] for rep in reports_as_chars)

    for report in reports:
        if len(report) == 1:
            safe_reports += 1
            continue

        safe = True
        pos = report[1] > report[0]
        for a,b in pairwise(report):
            if a == b or pos != (b > a):
                safe = False
                break

            diff = abs(b - a)
            if diff > 3:
                safe = False
                break

        if safe:
            safe_reports += 1

print(safe_reports)