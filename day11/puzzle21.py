from typing import Self

BLINK_COUNT = 25

input_file = 'input.txt'

class Stone:
    def __init__(self, val: int, nxt: Self = None):
        self.val = val
        self.next = nxt

    # return True if we duplicated and should skip the next node
    def update(self) -> bool:
        s = str(self.val)

        if self.val == 0:
            self.val = 1
        elif len(s) % 2 == 0:
            half = len(s) // 2
            s1 = s[:half]
            s2 = s[half:]
            self.val = int(s1)

            cls = self.__class__
            self.next = cls(int(s2), self.next)
            return True
        else:
            self.val *= 2024
        return False

    def __repr__(self):
        return f"Stone({self.val})"

dummy = Stone(-1)
last = dummy

with open(input_file) as f:
    line = f.readline().rstrip()
    nums = line.split()
    for num in nums:
        last.next = Stone(int(num))
        last = last.next

for _ in range(BLINK_COUNT):
    ptr = dummy.next
    skip_next = False
    while ptr:
        if not skip_next:
            if ptr.update():
                skip_next = True
        else:
            skip_next = False
        ptr = ptr.next

# count stones
ptr = dummy.next
res = 0
while ptr:
    res += 1
    ptr = ptr.next

print(res)