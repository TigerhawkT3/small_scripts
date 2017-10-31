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
    def reverse(self):
        self._iter, self._reviter = self._reviter, self._iter
        self.pop, self.popleft = self.popleft, self.pop
        self.appendleft, self.append = self.append, self.appendleft
    def insert(self, i, element):
        i = min(self.quantity, max(i, -self.quantity))
        if i in (0, -self.quantity):
            self.appendleft(element)
            return
        if i == self.quantity:
            self.append(element)
            return
        if i < 0:
            i += self.quantity
        if i < self.quantity//2:
            iterator = self._iter()
        else:
            iterator = self._reviter()
            i = abs(i - self.quantity)
        first = next(iterator)
        n = Node()
        for idx in range(i):
            current, n = n, next(iterator)
        temp = Node(element)
        if current.next is current.prior is None:
            node = first
        else:
            node = current
        if node.next is n:
            node.next = temp
            temp.prior = node
            temp.next = n
            n.prior = temp
        elif node.prior is n:
            node.prior = temp
            temp.next = node
            temp.prior = n
            n.next = temp
    def remove(self):
        pass
    def rotate(self):
        pass
    def __str__(self):
        return 'DQ({})'.format(', '.join(map(repr, self)))
    def __repr__(self):
        return repr(str(self))
    def _iter(self):
        current = self.first
        while current:
            yield current
            current = current.next
    def __iter__(self):
        for item in self._iter():
            yield item.element
    def _reviter(self):
        current = self.last
        while current:
            yield current
            current = current.prior
    def __reversed__(self):
        for item in self._reviter():
            yield item.element
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
    for i in range(-10, 10):
        d = DQ(*'abcdefg')
        d.insert(i, 5)
        print(i, d)
    d = DQ()
    d.insert(-5, 0)
    print(d)
    d.insert(-1, 1)
    print(d)
    d.insert(-1, 2)
    print(d)