input_file = r'input_short.txt'

safe_reports = 0
with open(input_file) as file:
    reports_as_chars = (line.split() for line in file)
    reports = ([int(x) for x in rep] for rep in reports_as_chars)

    for report in reports:
        if len(report) == 1:
            safe_reports += 1
            continue

        # try a monotonic increasing stack
        s = []
        removals = 0
        for x in report:
            safe = True
            while s and (x <= s[-1] or abs(x - s[-1]) > 3):
                s.pop()
                removals += 1
                if removals >= 2:
                    safe = False
                    break
            s.append(x)

            if not safe:
                break
        else:
            safe_reports += 1
            break

        # try a monotonic decreasing stack
        s.clear()
        removals = 0
        for x in report:
            safe = True
            while s and (x >= s[-1] or abs(x - s[-1]) > 3):
                s.pop()
                removals += 1
                if removals >= 2:
                    safe = False
                    break
            s.append(x)

            if not safe:
                break
        else:
            safe_reports += 1

print(safe_reports)