class DQ:
    def __init__(self, *items):
        self.count = 0
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
        self.count += 1
        return self, item
    def pop(self):
        temp = self.last
        if not temp:
            return self, None
        self.last = self.last.prior
        if self.last:
            self.last.next = None
        self.count -= 1
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
        self.count += 1
        return self, item
    def popleft(self):
        temp = self.first
        if not temp:
            return self, None
        self.first = self.first.next
        if self.first:
            self.first.prior = None
        self.count -= 1
        if not self:
            self.last = None
        return self, temp.element
    def __str__(self):
        return 'DQ({})'.format(', '.join(map(repr, self)))
    def __repr__(self):
        return repr(str(self))
    def __iter__(self):
        if not self.first:
            return iter('')
        current = self.first
        while current.next:
            yield current.element
            current = current.next
        yield current.element
    def __len__(self):
        return self.count
    def __bool__(self):
        return bool(len(self))
    def __add__(self, other):
        return DQ(*self, *other)

class Node:
    def __init__(self, element=None):
        self.next = self.prior = None
        self.element = element
    def __str__(self):
        return str(self.element)
    def __repr__(self):
        return 'Node({})'.format(repr(self.element))

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