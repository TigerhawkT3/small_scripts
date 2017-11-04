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
        return temp.element
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
        return temp.element
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
    def _neighbors(self, i):
        i = min(self.quantity, max(i, -self.quantity))
        if i < 0:
            i += self.quantity
        if not i or i == self.quantity:
            if not i:
                it = self._iter()
            else:
                it = self._reviter()
            try:
                current = next(it)
            except StopIteration:
                current = n = None
            else:
                try:
                    n = next(it)
                except StopIteration:
                    n = None
            if not i:
                return None, current, n
            else:
                return n, current, None
        if i < self.quantity//2:
            iterator = self._iter()
        else:
            iterator = self._reviter()
            i = abs(i - self.quantity)
        for idx in range(i):
            current = next(iterator)
        n = next(iterator)
        before,after = [n, current][::-(current.next is n) or 1]
        return before, current, after
    def insert(self, i, element):
        before, current, after = self._neighbors(i)
        if not before:
            self.appendleft(element)
            return
        if not after:
            self.append(element)
            return
        e = Node(element)
        e.prior, e.next = before, after
        before.next = after.prior = e
        self.quantity += 1
    def remove(self, item):
        for node in self._iter():
            if node.element == item:
                if node.prior:
                    node.prior.next = node.next
                else:
                    self.first = node.next
                if node.next:
                    node.next.prior = node.prior
                else:
                    self.last = node.prior
                self.quantity -= 1
                return
        raise ValueError(f'{repr(item)} not in deque')
    def rotate(self, i):
        if not self.quantity:
            return
        i %= self.quantity
        if not i:
            return
        if i < self.quantity//2:
            pop = self.pop
            append = self.appendleft
        else:
            pop = self.popleft
            append = self.append
            i = self.quantity - i
        for _ in range(i):
            append(pop())
    def rotate2(self, i):
        # this doesn't work yet. don't use it.
        if not self.quantity:
            return
        i = -(i%self.quantity)
        if not i:
            return
        before, current, after = self._neighbors(i)
        before.next = None
        self.last.next = self.first
        self.first.prior = self.last
        self.first = current
        current.prior = None
        self.last = before
        before.next = None
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
    d = DQ(*'abcde')
    for i in [1, -1, 3, -3, 7, -7]:
        d.rotate(i)
        print(*d, sep='')