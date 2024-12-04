input_file = r'input.txt'

def valid_report(report: list, start: int, allowed_removals: int, sign: int) -> bool:
    for i in range(start+1, len(report)):
        diff = (report[i] - report[i-1]) * sign
        if 1 <= diff <= 3:
            continue

        if not allowed_removals: return False
        # check if we can keep i by removing i-1
        if i > 1 and 1 <= (report[i] - report[i-2]) * sign <= 3:
            if valid_report(report, i, allowed_removals - 1, sign):
                return True

        # check if we can remove i
        if i + 1 < len(report) and 1 <= (report[i+1] - report[i-1]) * sign <= 3:
            if valid_report(report, i+1, allowed_removals - 1, sign):
                return True

        # if we're at the start, then just remove it and keep going
        if i == 1 and allowed_removals:
            return valid_report(report, 1, allowed_removals - 1, sign)

        # if we're at the last and have a removal remaining, then just remove it
        if i == len(report) - 1 and allowed_removals:
            return True

        # we cannot remove anything, so impossible
        return False

    return True



safe_reports = 0
with open(input_file) as file:
    reports_as_chars = (line.split() for line in file)
    reports = ([int(x) for x in rep] for rep in reports_as_chars)
    # reports_sloped = ([b-a for a, b in pairwise(report)] for report in reports)

    for report in reports:
        if len(report) == 1:
            safe_reports += 1
            continue

        if (valid_report(report, 0, 1, 1) or
                valid_report(report, 0, 1, -1)):
            safe_reports += 1


print(safe_reports)