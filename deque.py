class DQ:
    def __init__(self, *items, maxlen=None):
        self.maxlen = maxlen
        self.quantity = 0
        self.first = self.last = None
        for item in items:
            self.append(item)
    def append(self, item):
        temp = self.last
        if temp:
            self.last.next = self.last = Node(item)
            self.last.prior = temp
        else:
            self.first = self.last = Node(item)
        self.quantity += 1
        if self.maxlen and self.quantity > self.maxlen:
            self.popleft()
        return self, item
    def pop(self):
        temp = self.last
        if not temp:
            return self, None
        self.last = self.last.prior
        if self.last:
            self.last.next = None
        self.quantity -= 1
        if not self:
            self.first = None
        return self, temp.element
    def appendleft(self, item):
        temp = self.first
        if temp:
            self.first.prior = self.first = Node(item)
            self.first.next = temp
        else:
            self.first = self.last = Node(item)
        self.quantity += 1
        if self.maxlen and self.quantity > self.maxlen:
            self.pop()
        return self, item
    def popleft(self):
        temp = self.first
        if not temp:
            return self, None
        self.first = self.first.next
        if self.first:
            self.first.prior = None
        self.quantity -= 1
        if not self:
            self.last = None
        return self, temp.element
    def clear(self):
        self.last = self.first = None
        self.quantity = 0
    def copy(self):
        return DQ(*self)
    def count(self, item):
        return sum(item==element for element in self)
    def extend(self, other):
        for item in other:
            self.append(item)
    def extendleft(self, other):
        for item in other:
            self.appendleft(item)
    def index(self, item, start=0, stop=0):
        stop = stop or self.quantity
        for idx,val in enumerate(self):
            if val==item and start<=idx<stop:
                return idx
        raise ValueError(f'{repr(item)} is not in deque between index {start} and {stop}')
    def __str__(self):
        return 'DQ({})'.format(', '.join(map(repr, self)))
    def __repr__(self):
        return repr(str(self))
    def __iter__(self):
        if not self.first:
            return iter('')
        current = self.first
        while current:
            yield current.element
            current = current.next
    def __len__(self):
        return self.quantity
    def __bool__(self):
        return bool(self.quantity)
    def __add__(self, other):
        return DQ(*self, *other)

class Node:
    def __init__(self, element=None, *args):
        self.next = self.prior = None
        self.element = element
    def __str__(self):
        return str(self.element)
    def __repr__(self):
        return f'Node({repr(self.element)}, {self.prior and "..."}, {self.next and "..."})'

if __name__ == '__main__':
    d = DQ()
    print(d.append(1))
    print(d.append(2))
    print(d.append(3))
    print(d+d)
    print(d.appendleft(4))
    print(d.appendleft(5))
    print(d.appendleft(6))
    print(d.popleft())
    print(d.pop())
    print(d.append(7))
    print(d.appendleft(8))
    print(d.popleft())
    print(d.popleft())
    print(d.popleft())
    print(d.popleft())
    print(d.pop())
    print(d.pop())
    print(d.append(9))
    print(d.appendleft(10))
    print(d.popleft())
    print(d.pop())
    print(d.popleft())
    print(d.append(11))
    print(repr(d.last))
    print(d.append(12))
    print(repr(d.last))
    d.clear()
    d.extend([1, 2, 3])
    d.extendleft([3, 4, 5, 6])
    print(d)
    e = d.copy()
    print(e)
    print(d.count(3), d.count(1), d.count(0))
    print(d.index(3))
    print(d.index(3, 4))
    print(d.index(0))