import collections
import timeit

class DQ:
    def __init__(self, *items, maxlen=None):
        self.maxlen = maxlen
        self.quantity = 0
        self.first = self.last = None
        self.forward = True
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
        if self.maxlen is not None and self.quantity > self.maxlen:
            self.popleft()
    def pop(self):
        temp = self.last
        if not temp:
            raise IndexError('pop from an empty deque')
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
        if self.maxlen is not None and self.quantity > self.maxlen:
            self.pop()
    def popleft(self):
        temp = self.first
        if not temp:
            raise IndexError('pop from an empty deque')
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
        return DQ(*self, maxlen=self.maxlen)
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
        self.forward = not self.forward
    def distance_to_index(self, i, q):
        i = -(i%q)
        return self.norm_index(i, q)
    def norm_index(self, i, q):
        i = min(q, max(i, -q))
        if i < 0:
            i += q
        return i
    def _neighbors(self, i):
        i = self.norm_index(i, self.quantity)
        if not self.quantity:
            return None, None, None
        if i == self.quantity:
            it = self._reviter()
            return next(it), None, None
        if self.quantity == 1:
            return None, self.first, None
        if not i:
            it = self._iter()
            return None, next(it), next(it)
        if i == self.quantity-1:
            it = self._reviter()
            current = next(it)
            return next(it), current, None
        if i < self.quantity//2:
            it = self._iter()
            for idx in range(i):
                before = next(it)
            current, after = next(it), next(it)
        else:
            it = self._reviter()
            for idx in range(self.quantity-i-1):
                after = next(it)
            current, before = next(it), next(it)
        return before, current, after
    def insert(self, i, element):
        if self.quantity == self.maxlen:
            raise IndexError('deque already at its maximum size')
        node = Node(element)
        before, current, after = self._neighbors(i)
        if current is None:
            self.append(element)
            return
        if self.forward:
            if before:
                before.next = node
            else:
                self.first = node
            if current:
                current.prior = node
            else:
                self.last = node
            node.prior, node.next = before, current
        else:
            if before:
                before.prior = node
            else:
                self.last = node
            if current:
                current.next = node
            else:
                self.first = Node
            node.next, node.prior = before, current
        self.quantity += 1
    def rotate(self, i):
        if self.quantity < 2:
            return
        idx = self.distance_to_index(i, self.quantity)
        if not idx:
            return
        before,current,after = self._neighbors(idx)
        self.last.next, self.first.prior = self.first, self.last
        if self.forward:
            before.next = current.prior = None
            self.first, self.last = current, before
        else:
            before.prior = current.next = None
            self.last, self.first = current, before
    def _remove_replace(self, choice, old, new, count):
        if count < 0:
            it = self._reviter()
            count = abs(count)
        else:
            it = self._iter()
        counter = 0
        for node in it:
            if (not count or counter < count) and node.element == old:
                if choice == 'remove':
                    if node.prior:
                        node.prior.next = node.next
                    else:
                        self.first = node.next
                    if node.next:
                        node.next.prior = node.prior
                    else:
                        self.last = node.prior
                    self.quantity -= 1
                else:
                    node.element = new
                counter += 1
        if not counter:
            raise ValueError(f'{repr(old)} not in deque')
    def remove(self, item, count=1):
        self._remove_replace('remove', item, None, count)
    def replace(self, old, new, count=1):
        self._remove_replace('replace', old, new, count)
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
        return DQ(*self, *other, maxlen=self.maxlen)
    def __iadd__(self, other):
        if self is other:
            other = other.copy()
        self.extend(other)
        return self
    def __contains__(self, item):
        for element in self:
            if element == item:
                return True
        return False
    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError(f"can't multiply sequence by non-int of type {repr(type(other))}")
        if other < 1:
            return DQ(maxlen=self.maxlen)
        temp = self.copy()
        for _ in range(other - 1):
            temp.extend(self)
        return temp
    def __imul__(self, other):
        if not isinstance(other, int):
            raise TypeError(f"can't multiply sequence by non-int of type {repr(type(other))}")
        if other < 1:
            self.clear()
        temp = tuple(self)
        for _ in range(other-1):
            self.extend(temp)
        return self

class Node:
    def __init__(self, element=None, *args):
        self.next = self.prior = None
        self.element = element
    def __str__(self):
        return str(self.element)
    def __repr__(self):
        return f'Node({repr(self.element)}, {self.prior and "..."}, {self.next and "..."})'

if __name__ == '__main__':
    d = DQ(*'abcd')
    e = collections.deque('abcd')
    d.reverse()
    e.reverse()
    for i,ele in zip((0,0,20,3,-2,20,-20),('efghijk')):
        d.reverse()
        e.reverse()
        d.insert(i, ele)
        e.insert(i, ele)
        if tuple(d) != tuple(e): print(tuple(d) , tuple(e))
    for i in (0, 1, -1, 3, -3, 5, -5, 20, -20):
        d.rotate(i)
        e.rotate(i)
        e.reverse()
        d.reverse()
        if tuple(d) != tuple(e): print(tuple(d) , tuple(e))
    d.extend('1223564678231234')
    for item in (('e', 'E'), ('2', '@'), ('2', '@', -1), ('3', '#', 0), ('4', '$', -1)):
        d.replace(*item)
    print(d)
    for ln in range(-1, 4):
        print(d*ln)
    print(d)
    d += d
    print(d)
    
    
    
    
    
    
    
    
    
    
    