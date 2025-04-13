def possible_pattern(pattern: str, towels: set[str]):
    longest_towel = max(len(towel) for towel in towels)

    # dp[i] is true if pattern[i...] is possible
    dp = [False] * (len(pattern)+1)
    # the empty string is always possible
    dp[-1] = True
    for i in range(len(pattern)-1, -1, -1):
        for j in range(i+1, min(i+longest_towel, len(pattern))+1):
            # if we can find a towel in our set which would result
            # in a string we know is possible, then this string is
            # also possible
            if dp[j] and pattern[i:j] in towels:
                dp[i] = True
                break
    # dp[0] is true if pattern[0...], or the entire pattern is possible
    return dp[0]

def main(path):
    with open(path) as f:
        towel_line = f.readline()
        towels_list = towel_line.rstrip().split(',')
        towels = {towel.strip() for towel in towels_list}

        f.readline()
        out = 0
        for pattern in f:
            print(f"Pattern {pattern.rstrip()} is ",end='')
            if possible_pattern(pattern.rstrip(), towels):
                out += 1
                print("possible")
            else:
                print("impossible")
    return out

if __name__ == '__main__':
    print("--- example output ---")
    print("total:", main('example.txt'))
    print("--- puzzle 37 output ---")
    print("total:", main('input.txt'))