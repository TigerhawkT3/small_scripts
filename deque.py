import multiprocessing as mp

class DQ:
    '''
    DQ([iterable[, maxlen]]) --> DQ object

    A list-like sequence optimized for data accesses near its endpoints.
    
    A pure Python implementation of collections.deque,
    with added features.
    '''
    def __init__(self, items=(), maxlen=None):
        '''
        Create a new deque with the optional given iterable
        items and optional maximum length maxlen.
        Parameters:
            items (iterable): any iterable object containing items to add to the deque
            maxlen (int, None): a maximum length for the deque. Default is None for unbounded.
        Returns:
            deque (DQ): a double-ended queue container
        '''
        self.plus = self.p = self.concatenate = self.concat = self.c = self.__call__
        if maxlen is not None:
            if not isinstance(maxlen, int):
                raise TypeError('an integer is required')
            if maxlen<0:
                raise ValueError('maxlen must be non-negative')
        self.maxlen = maxlen
        self.quantity = 0
        self.invoke_mp = 150
        self.first = self.last = None
        self.forward = True
        for item in items:
            self.append(item)
    def append(self, item):
        '''
        Adds the given item to the end (right side) of the deque.
        Parameters:
            item (object): any item to add to the deque
        Returns:
            None
        '''
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
        '''
        Remove and return the item at the end (right side) of the deque.
        Raises IndexError if the deque is empty.
        Returns:
            item (object): the popped item
        '''
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
        '''
        Adds the given item to the front (left side) of the deque.
        Parameters:
            item (object): any item to add to the deque
        Returns:
            None
        '''
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
        '''
        Remove and return the item at the front (left side) of the deque.
        Raises IndexError if the deque is empty.
        Returns:
            item (object): the popped item
        '''
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
        '''
        Removes all items from the deque.
        Returns:
            None
        '''
        self.last = self.first = None
        self.quantity = 0
    def copy(self):
        '''
        Returns a shallow copy of the deque.
        Returns:
            deque (DQ): a new deque holding the same elements as this one
        '''
        return type(self)(self, maxlen=self.maxlen)
    def count(self, item):
        '''
        Return the number of items in the deque equal to the passed item.
        Parameters:
            item (object): the object to count (by equality)
        Returns:
            quantity (int): the number of objects equal to the passed item
        '''
        return sum(item==element for element in self)
    def extend(self, other):
        '''
        Append every item in iterable other to the end (right side) of this deque.
        Parameters:
            other (iterable): the object over which to iterate and whose contents
                              will be added to this deque
        Returns:
            None
        '''
        if self is other:
            other = tuple(other)
        for item in other:
            self.append(item)
    def extendleft(self, other):
        '''
        Append every item in iterable other to the front (left side) of this deque.
        Note that the objects will appear in reverse order.
        Parameters:
            other (iterable): the object over which to iterate and whose contents
                              will be added to this deque
        Returns:
            None
        '''
        for item in other:
            self.appendleft(item)
    def index(self, item, start=0, stop=0):
        '''
        Return the index of the first object between start and stop equal to the passed item.
        Raises ValueError if the item is not found.
        Parameters:
            item (object): the item whose index to locate
            start (int): the (optional) index at which to begin searching for the item
            stop (int): the (optional) index at which to stop searching for the item
        '''
        stop = stop or self.quantity
        for idx,val in enumerate(self):
            if val==item and start<=idx<stop:
                return idx
            if idx == stop:
                break
        raise ValueError(f'{repr(item)} is not in deque between index {start} and {stop}')
    def reverse(self):
        '''
        Reverses the deque in place.
        Returns:
            None
        '''
        self._iter, self._reviter = self._reviter, self._iter
        self.pop, self.popleft = self.popleft, self.pop
        self.appendleft, self.append = self.append, self.appendleft
        self._insert_after, self._insert_before = self._insert_before, self._insert_after
        self.forward = not self.forward
    def distance_to_index(self, i, q):
        '''
        Converts a given point i in or around a deque of length q to an index
        within the deque. Used for DQ.rotate.
        Parameters:
            i (int): location of point
            q (int): length of deque
        Returns:
            result (int): index within the deque where a rotate would manifest
        '''
        i = -(i%q)
        return self.norm_index(i, q)
    def norm_index(self, i, q):
        '''
        Return the real index 0 <= index <= len(deque) for any integer index.
        Parameters:
            i (int): index to normalize
            q (int): length of deque
        Returns:
            result (int): normalized index
        '''
        i = min(q, max(i, -q))
        if i < 0:
            i += q
        return i
    def _neighbors(self, i):
        '''
        Return the Node at a given index as well as its immediate neighbors to
        the left and right. Each such Node that does not exist will appear as None.
        Parameters:
            i (int): index for desired Node
        Returns:
            result (tuple): the three Node objects centered on the given index.
                            A None appears if there is no Node in that location.
        '''
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
        '''
        Returns the element at the given index or the sub-deque described by the given slice.
        Parameters:
            i (int, slice): an integer index or a slice of integers
        Returns:
            result (object, DQ): the desired element or deque of elements
        '''
        return self._getsetdel(i, None, 'get')
    def __setitem__(self, i, element):
        '''
        Assigns a new element at the given index or new elements at the indices described
        by the given slice.
        Parameters:
            i (int, slice): an integer index or a slice of integers
        Returns:
            None
        '''
        self._getsetdel(i, element, 'set')
    def __delitem__(self, i):
        '''
        Deletes the item at the given index or all items at the indices described
        by the given slice.
        Parameters:
            i (int, slice): an integer index or a slice of integers
        Returns:
            None
        '''
        self._getsetdel(i, None, 'del')
    def _slice(self, s):
        '''
        Yields Nodes from the deque, described by the given slice s.
        Parameters:
            s (slice): a slice of integers
        Yields:
            node (Node): Node objects described by the given slice
        '''
        r = range(*s.indices(self.quantity))
        idx = r.start
        step = r.step
        if idx not in r:
            return
        _, current, _ = self._neighbors(idx)
        it = (self._iter if step>0 else self._reviter)(current)
        current = next(it)
        while idx in r:
            yield current
            for _ in range(abs(step)):
                try:
                    current = next(it)
                except StopIteration:
                    break
            idx += step
    def _getsetdel(self, i, element, choice):
        '''
        Handles the logic for __getitem__, __setitem__, and __delitem__.
        Parameters:
            i (int, slice): an integer index or a slice of integers
            element (object, iterable): the element or iterable of elements to assign
            choice (str): 'get' to indicate __getitem__, 'set' to indicate __setitem__,
                             or 'del' to indicate __delitem__
        Returns:
            result (object, None, DQ): a single element (for 'get' at an index),
                                       None (for 'set' or 'del'),
                                       or a deque (for 'get' with a slice)
        '''
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
                self._remove_node(current)
            else:
                raise ValueError("choice must be 'get', 'set', or 'del'")
        if isinstance(i, slice):
            if choice == 'get':
                return type(self)(node.element for node in self._slice(i))
            elif choice == 'set':
                if not hasattr(element, '__len__'):
                    element = tuple(element)
                slc = self._slice(i)
                elements = iter(element)
                r = i.indices(self.quantity)
                start = r[0]
                step = r[2]
                length = len(range(*r))
                if step != 1 and length != len(element):
                    raise ValueError('attempt to assign sequence of size '
                                    f'{length} to extended slice of size {len(element)}')
                if length >= len(element):
                    for value,node in zip(elements, slc):
                        node.element = value
                else:
                    for node,value in zip(slc, elements):
                        node.element = value
                if step != 1:
                    return
                for node in slc:
                    self._remove_node(node)
                if length:
                    for value in elements:
                        node = self._insert_after(node, value)
                elif self.quantity:
                    before, node, _ = self._neighbors(r[0])
                    if node:
                        try:
                            node = self._insert_before(node, next(elements))
                        except StopIteration:
                            pass
                    else:
                        node = before
                    for value in elements:
                        node = self._insert_after(node, value)
                else:
                    self.extend(elements)
            elif choice == 'del':
                for node in self._slice(i):
                    self._remove_node(node)
            else:
                raise ValueError("choice must be 'get', 'set', or 'del'")
    def insert(self, i, element):
        '''
        Inserts the given element at the given index i.
        Parameters:
            i (int): the index at which to insert the element
            element (object): the object to insert at the given index
        Returns:
            None
        '''
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
        '''
        Rotates the deque i steps to the right. If i is negative, rotate
        to the left. Rotating one step to the right is equivalent to:
        d.appendleft(d.pop()). When i is 0 or the deque has fewer than
        two items, this method has no effect.
        Parameters:
            i (int): the distance to rotate the deque
        Returns:
            None
        '''
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
    def _remove_node(self, node):
        '''
        Remove a given Node from the deque. Requires a Node object
        that is present in the deque.
        Parameters:
            node (Node): the Node to remove from the deque
        Returns:
            None
        '''
        if node.prior:
            node.prior.next = node.next
        else:
            self.first = node.next
        if node.next:
            node.next.prior = node.prior
        else:
            self.last = node.prior
        self.quantity -= 1
    def _insert_after(self, node, value):
        '''
        Inserts a new Node with the given value after the given Node.
        Parameters:
            node (Node): the Node after which to add our new value
            value (object): the value to add after the given Node
        Returns:
            None
        '''
        self.quantity += 1
        n = Node(value)
        if node.next:
            other = node.next
            node.next = other.prior = n
            n.prior, n.next = node, other
        else:
            node.next = self.last = n
            n.prior = node
        return n
    def _insert_before(self, node, value):
        '''
        Inserts a new Node with the given value before the given Node.
        Parameters:
            node (Node): the Node before which to add our new value
            value (object): the value to add before the given Node
        Returns:
            None
        '''
        self.quantity += 1
        n = Node(value)
        if node.prior:
            other = node.prior
            node.prior = other.next = n
            n.prior, n.next = other, node
        else:
            node.prior = self.first = n
            n.next = node
        return n
    def _remove_replace(self, choice, old, new, count):
        '''
        Handles the logic for the remove and replace methods.
        Parameters:
            choice (str): 'remove' for remove or 'replace' for replace
            old (object): the element to replace (by equality) for 'replace'
            new (object): the new element added by 'replace'
            count (int): the number of removals or replacements to handle.
                         A count of 0 performs these operations without limit,
                         while a positive count goes from left to right and
                         a negative count goes from right to left.
        Returns:
            None
        '''
        if count < 0:
            it = self._reviter()
            count = abs(count)
        else:
            it = self._iter()
        counter = 0
        for node in it:
            if (not count or counter < count) and node.element == old:
                if choice == 'remove':
                    self._remove_node(node)
                else:
                    node.element = new
                counter += 1
        if not counter:
            raise ValueError(f'{repr(old)} not in deque')
    def remove(self, item, count=1):
        '''
        Remove count instances of the given item from the deque.
        A positive count searches from the left, a negative count
        searches from the right, and a count of zero removes
        all instances.
        Parameters:
            item (object): the item to search for and remove
            count (int): the number of removals to handle.
                         A count of 0 performs removals without limit,
                         while a positive count goes from left to right and
                         a negative count goes from right to left.
        Returns:
            None
        '''
        self._remove_replace('remove', item, None, count)
    def replace(self, old, new, count=0):
        '''
        Replace count instances of the given item old from the
        deque with given item new.
        A positive count searches from the left, a negative count
        searches from the right, and a count of zero replaces
        all instances.
        Parameters:
            old (object): the item to search for and replace
            new (object): the item that replaces the given old item
            count (int): the number of replacements to handle.
                         A count of 0 performs replacements without limit,
                         while a positive count goes from left to right and
                         a negative count goes from right to left.
        Returns:
            None
        '''
        self._remove_replace('replace', old, new, count)
    def __str__(self):
        '''
        Returns the string representation of the deque.
        Can be evaluated with eval back into an equivalent deque.
        Returns:
            result (str): the deque as a string
        '''
        return 'DQ([{}])'.format(', '.join('DQ([...])' if item is self else repr(item) for item in self))
    def __repr__(self):
        '''
        Returns the string representation of the deque.
        Can be evaluated with eval back into an equivalent deque.
        Returns:
            result (str): the deque as a string
        '''
        return str(self)
    def _iter(self, current=None):
        '''
        Yields a Node for each item in the deque, from beginning (left) to end (right).
        Parameters:
            current (Node, None): a Node to start from, or None for all items
        Yields:
            node (Node): each node from the given current Node onward, or all Nodes
        '''
        if current is None:
            current = self.first
        while current:
            yield current
            current = current.next
    def __iter__(self):
        '''
        Yields each element in the deque, from beginning (left) to end (right).
        Yields:
            element (object): each element in the deque, from beginning to end
        '''
        for item in self._iter():
            yield item.element
    def _reviter(self, current=None):
        '''
        Yields a Node for each item in the deque, from end (right) to beginning (left).
        Parameters:
            current (Node, None): a Node to start from, or None for all items
        Yields:
            node (Node): each node from the given current Node backward, or all Nodes
        '''
        if current is None:
            current = self.last
        while current:
            yield current
            current = current.prior
    def __reversed__(self):
        '''
        Yields each element in the deque, from end (right) to beginning (left).
        Yields:
            element (object): each element in the deque, from end to beginning
        '''
        for item in self._iter():
            yield item.element
        for item in self._reviter():
            yield item.element
    def __len__(self):
        '''
        Returns the length of the deque.
        Returns:
            length (int): length of the deque
        '''
        return self.quantity
    def __bool__(self):
        '''
        Returns the boolean evaluation of the deque. A deque is falsey if empty,
        or truthy otherwise.
        Returns:
            result (bool): truthiness of the deque
        '''
        return bool(self.quantity)
    def __call__(self, *args):
        '''
        Concatenate an iterable onto this deque, then return it.
        Parameters:
            other (iterable): the iterable to add to this deque
        Returns:
            deque (DQ): this deque
        Examples:
            a = DQ('123')
            b = DQ('456')
            c = DQ('789')
            DQ()(a, b, c) # new deque 123456789
            DQ()(a)(b)(c) # new deque 123456789
            a(b)(c) # a is now 123456789
            a(b(c)) # a is now 123456789, b is now 456789
        '''
        for other in args:
            self.extend(other)
        return self
    def __contains__(self, item):
        '''
        Return whether item is in the deque.
        Parameters:
            item (object): item to search for
        Returns:
            result (bool): whether item in deque
        '''
        for element in self:
            if element == item:
                return True
        return False
    def __matmul__(self, other):
        '''
        Returns the result of a matrix multiplication of self by other.
        Row vectors and column vectors are promoted to 2D matrices,
        and their result is demoted back down after calculation.
        In A@B, with A being m height * n width, B must be n
        height * p width. Multiprocessing is invoked only when
        max(m,n,p) >= deque.invoke_mp to avoid large setup overhead.
        The default value of deque.invoke_mp is 150, the break-even
        point for square matrices of small integers.
        Parameters:
            other (iterable): vector or matrix to multiply
        Returns:
            result (DQ, int): a 2D deque matrix, 1D deque, or
                              integer scalar
        '''
        try:
            n1 = len(self[0])
        except TypeError:
            self = type(self)([self])
            n1 = len(self[0])
            coerced_self = True
        else:
            coerced_self = False
        m = len(self)
        n2 = len(other)
        if n1 != n2:
            raise ValueError(f'Width of left operand must match height of right operand (currently {n1} and {n2}).')
        try:
            p = len(other[0])
        except TypeError:
            other = tuple([i] for i in other)
            p = len(other[0])
            coerced_other = True
        else:
            coerced_other = False
        m,n1,n2,p = len(self), len(self[0]), len(other), len(other[0])
        n = n1
        if max(m,n,p) < self.invoke_mp:
            result = type(self)(type(self)(sum(a*b for a,b in zip(row,col)) for col in zip(*other)) for row in self)
        else:
            self.other = other
            size = n//mp.cpu_count()
            with mp.Pool() as p:
                result = type(self)(p.imap(self.findrow, self, size))
            del self.other
        if coerced_self and not coerced_other:
            return result[0]
        elif not coerced_self and coerced_other:
            return type(self)(i[0] for i in result)
        elif coerced_self and coerced_other:
            return result[0][0]
        else:
            return result
    def findrow(self, row):
        '''
        Returns the matrix multiplication result of A*B for a
        single row of A. Matrix B is stored in deque.other.
        Parameters:
            row (iterable): a single row of matrix A
        Returns:
            deque (DQ): a deque of this row's matrix multiplication
                        result with deque.other
        '''
        return type(self)(sum(a*b for a,b in zip(row,col)) for col in zip(*self.other))
    def __rmatmul__(self, other):
        '''
        Returns the result of a matrix multiplication of self by other.
        For reflected operands. See deque.__matmul__ for details.
        Parameters:
            other (iterable): vector or matrix to multiply
        Returns:
            result (DQ, int): a 2D deque matrix, 1D deque, or
                              integer scalar
        '''
        return type(self).__matmul__(other, self)
    def __imatmul__(self, other):
        '''
        Implement self@=other. Syntactic sugar for deque = deque @ other.
        The old reference for this deque is discarded without any
        attempt to modify this deque in place, as the result
        might have different dimensions, shape, or even type.
        Parameters:
            other (iterable): vector or matrix to multiply
        Returns:
            result (DQ, int): a 2D deque matrix, 1D deque, or
                              integer scalar
        '''
        return self@other
    def __add__(self, other):
        '''
        Return the result of elementwise evaluation with
        the + operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) + (c, d, e) -> (a+c, b+d)
        '''
        return type(self)(a+b for a,b in zip(self, other))
    def __radd__(self, other):
        '''
        Reflected operator version of deque.__add__.
        '''
        return type(self)(a+b for a,b in zip(other, self))
    def __iadd__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__add__.
        '''
        for node,value in zip(self._iter(), other):
            node.element += value
    def __sub__(self, other):
        '''
        Return the result of elementwise evaluation with
        the - operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) - (c, d, e) -> (a-c, b-d)
        '''
        return type(self)(a-b for a,b in zip(self, other))
    def __rsub__(self, other):
        '''
        Reflected operator version of deque.__sub__.
        '''
        return type(self)(a-b for a,b in zip(other, self))
    def __isub__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__sub__.
        '''
        for node,value in zip(self._iter(), other):
            node.element -= value
    def __mul__(self, other):
        '''
        Returns a new deque consisting of the current deque's references
        repeated other times, or a new deque of the elementwise
        multiplication of this deque and iterable other.
        Parameters:
            other (int, iterable): number of times to repeat this deque,
                                   or iterable for elementwise multiplication
        Returns:
            deque (DQ): the resulting deque
        '''
        if isinstance(other, int):
            if other < 1:
                return type(self)(maxlen=self.maxlen)
            temp = self.copy()
            for _ in range(other - 1):
                temp.extend(self)
            return temp
        try:
            return type(self)(a*b for a,b in zip(self, other))
        except TypeError:
            pass
        raise TypeError(f"can't multiply sequence by non-(int/iterable) of type {repr(type(other))}")
    def __rmul__(self, other):
        '''
        Returns a new deque consisting of the current deque's references
        repeated other times, or a new deque of the elementwise
        multiplication of this deque and iterable other. For reflected operands.
        Parameters:
            other (int, iterable): number of times to repeat this deque,
                                   or iterable for elementwise multiplication
        Returns:
            deque (DQ): the resulting deque
        '''
        if isinstance(other, int):
            return self*other
        try:
            return type(self)(a*b for a,b in zip(other, self))
        except TypeError:
            pass
        raise TypeError(f"can't multiply sequence by non-(int/iterable) of type {repr(type(other))}")
    def __imul__(self, other):
        '''
        Expands the current deque to contain other repeats of its references,
        or update this deque's elements to the elementwise multiplication
        of this deque and iterable other.
        Parameters:
            other (int, iterable): number of times to repeat this deque,
                                   or iterable for elementwise multiplication
        Returns:
            deque (DQ): this deque
        '''
        if isinstance(other, int):
            if other < 1:
                self.clear()
            temp = tuple(self)
            for _ in range(other-1):
                self.extend(temp)
            return self
        try:
            for node,value in zip(self._iter(), other):
                node.element *= value
        except TypeError:
            pass
        raise TypeError(f"can't multiply sequence by non-(int/iterable) of type {repr(type(other))}")
    def __truediv__(self, other):
        '''
        Return the result of elementwise evaluation with
        the / operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) / (c, d, e) -> (a/c, b/d)
        '''
        return type(self)(a/b for a,b in zip(self, other))
    def __rtruediv__(self, other):
        '''
        Reflected operator version of deque.__truediv__.
        '''
        return type(self)(a/b for a,b in zip(other, self))
    def __itruediv__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__truediv__.
        '''
        for node,value in zip(self._iter(), other):
            node.element /= value
    def __floordiv__(self, other):
        '''
        Return the result of elementwise evaluation with
        the // operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) // (c, d, e) -> (a//c, b//d)
        '''
        return type(self)(a//b for a,b in zip(self, other))
    def __rfloordiv__(self, other):
        '''
        Reflected operator version of deque.__floordiv__.
        '''
        return type(self)(a//b for a,b in zip(other, self))
    def __ifloordiv__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__floordiv__.
        '''
        for node,value in zip(self._iter(), other):
            node.element //= value
    def __mod__(self, other):
        '''
        Return the result of elementwise evaluation with
        the % operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) % (c, d, e) -> (a%c, b%d)
        '''
        return type(self)(a%b for a,b in zip(self, other))
    def __rmod__(self, other):
        '''
        Reflected operator version of deque.__mod__.
        '''
        return type(self)(a%b for a,b in zip(other, self))
    def __imod__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__mod__.
        '''
        for node,value in zip(self._iter(), other):
            node.element %= value
    def __divmod__(self, other):
        '''
        Return the result of elementwise evaluation with
        the divmod function. Equivalent to DQ(map(divmod, deque, other)).
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): divmod((a, b), (c, d, e)) -> (divmod(a,c), divmod(b,d))
        '''
        return type(self)(map(divmod, self, other))
    def __rdivmod__(self, other):
        '''
        Reflected operator version of deque.__divmod__.
        '''
        return type(self)(map(divmod, other, self))
    def __pow__(self, other):
        '''
        Return the result of elementwise evaluation with
        the ** operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) ** (c, d, e) -> (a**c, b**d)
        '''
        return type(self)(a**b for a,b in zip(self, other))
    def __rpow__(self, other):
        '''
        Reflected operator version of deque.__pow__.
        '''
        return type(self)(a**b for a,b in zip(other, self))
    def __ipow__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__pow__.
        '''
        for node,value in zip(self._iter(), other):
            node.element **= value
    def __lshift__(self, other):
        '''
        Return the result of elementwise evaluation with
        the << operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) << (c, d, e) -> (a<<c, b<<d)
        '''
        return type(self)(a<<b for a,b in zip(self, other))
    def __rlshift__(self, other):
        '''
        Reflected operator version of deque.__lshift__.
        '''
        return type(self)(a<<b for a,b in zip(other, self))
    def __ilshift__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__lshift__.
        '''
        for node,value in zip(self._iter(), other):
            node.element <<= value
    def __rshift__(self, other):
        '''
        Return the result of elementwise evaluation with
        the >> operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) >> (c, d, e) -> (a>>c, b>>d)
        '''
        return type(self)(a>>b for a,b in zip(self, other))
    def __rrshift__(self, other):
        '''
        Reflected operator version of deque.__rshift__.
        '''
        return type(self)(a>>b for a,b in zip(other, self))
    def __irshift__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__rshift__.
        '''
        for node,value in zip(self._iter(), other):
            node.element >>= value
    def __and__(self, other):
        '''
        Return the result of elementwise evaluation with
        the & operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) & (c, d, e) -> (a&c, b&d)
        '''
        return type(self)(a&b for a,b in zip(self, other))
    def __rand__(self, other):
        '''
        Reflected operator version of deque.__and__.
        '''
        return type(self)(a&b for a,b in zip(other, self))
    def __iand__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__and__.
        '''
        for node,value in zip(self._iter(), other):
            node.element &= value
    def __xor__(self, other):
        '''
        Return the result of elementwise evaluation with
        the ^ operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) ^ (c, d, e) -> (a^c, b^d)
        '''
        return type(self)(a^b for a,b in zip(self, other))
    def __rxor__(self, other):
        '''
        Reflected operator version of deque.__xor__.
        '''
        return type(self)(a^b for a,b in zip(other, self))
    def __ixor__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__xor__.
        '''
        for node,value in zip(self._iter(), other):
            node.element ^= value
    def __or__(self, other):
        '''
        Return the result of elementwise evaluation with
        the | operator.
        Parameters:
            other (iterable): the other iterable to operate on
        Returns:
            deque (DQ): (a, b) | (c, d, e) -> (a|c, b|d)
        '''
        return type(self)(a|b for a,b in zip(self, other))
    def __ror__(self, other):
        '''
        Reflected operator version of deque.__or__.
        '''
        return type(self)(a|b for a,b in zip(other, self))
    def __ior__(self, other):
        '''
        Augmented assignment version (in-place modification) of deque.__or__.
        '''
        for node,value in zip(self._iter(), other):
            node.element |= value
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
        return len(self)==len(other) and all(a==b for a,b in zip(self,other))
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
    '''
    Node([element]) --> Node object
    
    A singleton container for objects in a deque.
    '''
    def __init__(self, element=None, *args):
        '''
        Initialize a new Node with an optional given element.
        Parameters:
            element (object): the element this Node should contain
        Returns:
            None (initializes)
        '''
        self.next = self.prior = None
        self.element = element
    def __str__(self):
        return 'Node(...)' if self is self.element else str(self.element)
    def __repr__(self):
        return (f'Node({"Node(...)" if self is self.element else repr(self.element)}, '
                f'{self.prior and "..."}, {self.next and "..."})')