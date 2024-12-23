from typing import Self

input_file = 'input.txt'

class DiskLocation:
    next_id = 0

    def __init__(self, size: int, file_id: int, nxt: Self = None, prev: Self = None):
        self.size = size
        self.id = file_id
        self.next = nxt
        self.prev = prev

    def append_file(self, size: int) -> Self:
        cls = self.__class__
        self.next = cls(size, cls.next_id, None, self)
        cls.next_id += 1
        return self.next

    def append_free_space(self, size: int) -> Self:
        # expand this block if this block is free space
        if self.id == -1:
            self.size += size
            return self

        # append a new block of free space after this block
        cls = self.__class__
        self.next = cls(size, -1, None, self)
        return self.next

    def remove_file(self) -> int:
        if self.id == -1:
            raise ValueError("Free space cannot be removed")

        ret = self.id
        self.id = -1

        # combine with previous if it's free space
        if self.prev and self.prev.id == -1:
            temp = self.prev
            self.prev = temp.prev
            if temp.prev:
                temp.prev.next = self
            self.size += temp.size
            del temp

        # combine with next if it's free space
        if self.next and self.next.id == -1:
            temp = self.next
            self.next = temp.next
            if temp.next:
                temp.next.prev = self
            self.size += temp.size
            del temp

        return ret

    def add_file(self, size: int, file_id: int) -> None:
        if self.id != -1:
            raise ValueError("File cannot be added over another file")
        if self.size < size:
            raise ValueError(f"Free space {self.size} is too small for file {file_id} of size {size}.")

        self.id = file_id
        if self.size == size:
            return

        free_space = self.size - size
        self.size = size

        cls = self.__class__
        nxt = self.next
        self.next = cls(free_space, -1, nxt, self)
        nxt.prev = self.next

    def is_free(self) -> bool:
        return self.id == -1

    def __repr__(self) -> str:
        return f"FileLocation({self.size}, {self.id}, {'?' if self.next else 'None'}, {'?' if self.prev else 'None'})"

with open(input_file) as f:
    disk_map = f.readline().rstrip()

attempt_move = []
dummy = DiskLocation(0, -2)
last = dummy
for i, d in enumerate(disk_map):
    if d == '0':
        continue
    if i % 2 == 0:
        last = last.append_file(int(d))
        attempt_move.append(last)
    else:
        last = last.append_free_space(int(d))

# move files one at a time
while attempt_move:
    file = attempt_move.pop()
    size, f_id = file.size, file.id
    ptr = dummy.next
    while ptr != file:
        if not ptr.is_free() or ptr.size < size:
            ptr = ptr.next
            continue
        ptr.add_file(size, f_id)
        file.remove_file()
        break

ptr = dummy.next
pos = 0
res = 0
while ptr:
    if ptr.is_free():
        pos += ptr.size
        ptr = ptr.next
        continue
    for _ in range(ptr.size):
        res += ptr.id * pos
        pos += 1
    ptr = ptr.next

print(res)