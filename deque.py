import collections
import timeit

class DQ:
    def __init__(self, *items, maxlen=None):
        if maxlen is not None:
            if not isinstance(maxlen, int):
                raise TypeError('an integer is required')
            if maxlen<0:
                raise ValueError('maxlen must be non-negative')
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
        return type(self)(*self, maxlen=self.maxlen)
    def count(self, item):
        return sum(item==element for element in self)
    def extend(self, other):
        if self is other:
            other = tuple(other)
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
    def __getitem__(self, i):
        return self._getsetdel(i, None, 'get')
    def __setitem__(self, i, element):
        self._getsetdel(i, element, 'set')
    def __delitem__(self, i):
        self._getsetdel(i, None, 'del')
    def _getsetdel(self, i, element, choice):
        if not (isinstance(i, int) or isinstance(i, slice)):
            raise TypeError(f'deque indices must be integers or int/None slices, not {repr(type(i))}')
        if isinstance(i, int):
            if not -self.quantity <= i < self.quantity:
                raise IndexError(f'deque assignment index {i} out of range {-self.quantity} to {self.quantity-1}')
            before, current, after = self._neighbors(i)
            if choice == 'get':
                return current.element
            elif choice == 'set':
                current.element = element
            elif choice == 'del':
                if self.forward:
                    if before:
                        before.next = after
                    else:
                        self.first = after
                    if after:
                        after.prior = before
                    else:
                        self.last = before
                else:
                    if before:
                        before.prior = after
                    else:
                        self.last = after
                    if after:
                        after.next = before
                    else:
                        self.first = before
            else:
                raise ValueError("choice must be 'get', 'set', or 'del'")
        if isinstance(i, slice):
            # incomplete
            if not all(isinstance(part, int) or part is None for part in (i.start, i.stop, i.step)):
                raise TypeError('slice indices must be integers or None (empty)')
            start, stop, step = i.start, i.stop, i.step
            step = step or 1
            if step < 1:
                start,stop = stop,start
            if start is None:
                pass
            else:
                start = self.norm_index(start, self.quantity)
            if stop is None:
                pass
            else:
                stop = self.norm_index(stop, self.quantity)
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
        return type(self)(*self, *other, maxlen=self.maxlen)
    def __iadd__(self, other):
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
            return type(self)(maxlen=self.maxlen)
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
    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        for a,b in zip(self, other):
            if a < b:
                return True
            if a > b:
                return False
        return len(self) < len(other)
    def __le__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        for a,b in zip(self, other):
            if a < b:
                return True
            if a > b:
                return False
        return len(self) <= len(other)
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return all(a==b for a,b in zip(self,other)) and len(self)==len(other)
    def __ne__(self, other):
        return not (self == other)
    def __gt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        for a,b in zip(self, other):
            if a > b:
                return True
            if a < b:
                return False
        return len(self) > len(other)
    def __ge__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        for a,b in zip(self, other):
            if a > b:
                return True
            if a < b:
                return False
        return len(self) >= len(other)

class Node:
    def __init__(self, element=None, *args):
        self.next = self.prior = None
        self.element = element
    def __str__(self):
        return str(self.element)
    def __repr__(self):
        return f'Node({repr(self.element)}, {self.prior and "..."}, {self.next and "..."})'

if __name__ == '__main__':
    d = DQ(*'abcdefghijk')
    e = collections.deque('abcdefghijk')
    for i in range(-len(d), len(d)):
        d[i], e[i] = e[i], d[i]
        if tuple(d) != tuple(e):
            print(i, d[i], e[i])
    print(d)
    del d[4]
    print(d)
    
    
    
    
    
    
    
    
    
    