def ways_to_make_pattern(pattern: str, towels: set[str]):
    longest_towel = max(len(towel) for towel in towels)

    # dp[i] is the amount of ways to make pattern[i...]
    dp = [0] * (len(pattern)+1)
    # the empty string has 1 way to make it (using nothing)
    dp[-1] = 1
    for i in range(len(pattern)-1, -1, -1):
        for j in range(i+1, min(i+longest_towel, len(pattern))+1):
            # if we can find a towel in our set which would result
            # in a string with `n` ways to make, then this string
            # has an additional `n` ways to make it

            if dp[j] > 0 and pattern[i:j] in towels:
                dp[i] += dp[j]
    # dp[0] is the amount of ways to make pattern[0...], or the entire pattern
    return dp[0]

def main(path):
    with open(path) as f:
        towel_line = f.readline()
        towels_list = towel_line.rstrip().split(',')
        towels = {towel.strip() for towel in towels_list}

        f.readline()
        out = 0
        for pattern in f:
            print(f"Pattern {pattern.rstrip()} has ",end='')
            ways = ways_to_make_pattern(pattern.rstrip(), towels)
            print(ways, "ways")
            out += ways

    return out

if __name__ == '__main__':
    print("--- example output ---")
    print("total:", main('example.txt'))
    print("--- puzzle 37 output ---")
    print("total:", main('input.txt'))