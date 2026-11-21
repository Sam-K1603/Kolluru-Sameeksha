import collections, copy, time


class Empty(Exception):
    pass


# Part A, Q2
def factorial(n):
    if n < 0: raise ValueError("n must be >= 0")
    return 1 if n == 0 else n * factorial(n - 1)

def linear_sum(n):
    if n < 0: raise ValueError("n must be >= 0")
    return 0 if n == 0 else n + linear_sum(n - 1)

def power(x, n):
    if n < 0: raise ValueError("n must be >= 0")
    return 1 if n == 0 else x * power(x, n - 1)

print("A-Q2:", factorial(5), linear_sum(10), power(2, 10))


# Part A, Q3
def reverse_in_place(S, start, stop, depth=0):
    print("  " * depth, start, stop, S)
    if start < stop - 1:
        S[start], S[stop - 1] = S[stop - 1], S[start]
        reverse_in_place(S, start + 1, stop - 1, depth + 1)

print("A-Q3:")
data = [1, 2, 3, 4, 5, 6]
reverse_in_place(data, 0, 6)


# Part A, Q4
def is_sorted(S, i=0, calls=None):
    if calls: calls[0] += 1
    if i >= len(S) - 1: return True
    if S[i] > S[i + 1]: return False
    return is_sorted(S, i + 1, calls)

best, worst = [0], [0]
is_sorted([9, 1, 2, 3], 0, best)
is_sorted([1, 2, 3, 4], 0, worst)
print("A-Q4: best-case calls", best[0], "| worst-case calls", worst[0])


# Part A, Q5
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

def fib_tree(n, depth, seen):
    seen[n] += 1
    print("    " * depth + "fib(%d)" % n)
    return n if n < 2 else fib_tree(n - 1, depth + 1, seen) + fib_tree(n - 2, depth + 1, seen)

print("A-Q5:")
seen = collections.Counter()
fib_tree(5, 0, seen)
print("calls per subproblem:", dict(seen))


# Part A, Q6
def fib_calls(n):
    return 1 if n < 2 else 1 + fib_calls(n - 1) + fib_calls(n - 2)

print("A-Q6:", [(n, fib_calls(n)) for n in (5, 10, 15, 20)])


# Part A, Q7
def hanoi(n, src, dst, spare, moves):
    if n == 0: return
    hanoi(n - 1, src, spare, dst, moves)
    moves.append((n, src, dst))
    hanoi(n - 1, spare, dst, src, moves)

moves = []
hanoi(3, "A", "C", "B", moves)
print("A-Q7:", len(moves), "moves:", moves)


# Part A, Q9
def sum_tail(S, i=0, acc=0):
    return acc if i == len(S) else sum_tail(S, i + 1, acc + S[i])

def sum_iterative(S):
    acc = 0
    for x in S: acc += x
    return acc

try:
    sum_tail(list(range(5000)))
except RecursionError:
    print("A-Q9: recursive version -> RecursionError (n stack frames)")
print("A-Q9: iterative version:", sum_iterative(range(10 ** 6)), "(O(1) stack)")


# Part B, Q2
original = [[1, 2], [3, 4]]
shallow, deep = copy.copy(original), copy.deepcopy(original)
original[0].append(99)
print("B-Q2: original", original, "| shallow", shallow, "| deep", deep)


# Part B, Q6
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("B-Q6: row 1", grid[1], "| column 2", [row[2] for row in grid])


# Part C, Q2
class ArrayStack:
    def __init__(self): self._data = []
    def __len__(self): return len(self._data)
    def is_empty(self): return not self._data
    def push(self, e): self._data.append(e)
    def top(self):
        if self.is_empty(): raise Empty("Stack is empty")
        return self._data[-1]
    def pop(self):
        if self.is_empty(): raise Empty("Stack is empty")
        return self._data.pop()

S = ArrayStack()
S.push(1); S.push(2)
print("C-Q2:", S.top(), S.pop(), S.pop(), S.is_empty())
try:
    S.pop()
except Empty as e:
    print("C-Q2: pop on empty stack ->", e)


# Part C, Q4
def reverse_with_stack(seq):
    S, out = ArrayStack(), []
    for x in seq:
        S.push(x); print("  push", x, S._data)
    while not S.is_empty():
        out.append(S.pop()); print("  pop ", out[-1], S._data)
    return out

print("C-Q4:", reverse_with_stack("ABC"))


# Part C, Q5
PAIRS = {")": "(", "]": "[", "}": "{"}

def balanced_stack(expr):
    S = ArrayStack()
    for ch in expr:
        if ch in "([{": S.push(ch)
        elif ch in PAIRS and (S.is_empty() or S.pop() != PAIRS[ch]): return False
    return S.is_empty()

def balanced_counting(expr):
    return all(expr.count(o) == expr.count(c) for c, o in PAIRS.items())

for expr in ["{[()]}", "([)]", ")("]:
    print("C-Q5:", expr, "stack:", balanced_stack(expr), "counting:", balanced_counting(expr))


# Part C, Q8
class ArrayQueue:
    def __init__(self): self._data, self._size, self._front = [None] * 4, 0, 0
    def __len__(self): return self._size
    def is_empty(self): return self._size == 0
    def first(self):
        if self.is_empty(): raise Empty("Queue is empty")
        return self._data[self._front]
    def dequeue(self):
        if self.is_empty(): raise Empty("Queue is empty")
        value, self._data[self._front] = self._data[self._front], None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return value
    def enqueue(self, e):
        if self._size == len(self._data): self._resize(2 * len(self._data))
        self._data[(self._front + self._size) % len(self._data)] = e
        self._size += 1
    def _resize(self, capacity):
        items = self.to_list()
        self._data, self._front = items + [None] * (capacity - len(items)), 0
    def to_list(self):
        return [self._data[(self._front + k) % len(self._data)] for k in range(self._size)]

Q = ArrayQueue()
for x in (1, 2, 3, 4): Q.enqueue(x)
Q.dequeue(); Q.dequeue(); Q.enqueue(5); Q.enqueue(6)
print("C-Q8:", Q.to_list(), "front =", Q._front)


# Part C, Q10
class ArrayDeque(ArrayQueue):
    def add_last(self, e): self.enqueue(e)
    def delete_first(self): return self.dequeue()
    def add_first(self, e):
        if self._size == len(self._data): self._resize(2 * len(self._data))
        self._front = (self._front - 1) % len(self._data)
        self._data[self._front] = e
        self._size += 1
    def delete_last(self):
        if self.is_empty(): raise Empty("Deque is empty")
        back = (self._front + self._size - 1) % len(self._data)
        value, self._data[back] = self._data[back], None
        self._size -= 1
        return value

D = ArrayDeque()
D.add_last(2); D.add_last(3); D.add_first(1); D.add_first(0)
print("C-Q10:", D.to_list(), D.delete_first(), D.delete_last(), D.to_list())


# Part C, Q11
def workload(add_first, add_last, del_first, del_last, n):
    for i in range(n): add_last(i)
    for i in range(n): add_first(i)
    for _ in range(n): del_first()
    for _ in range(n): del_last()

def run_list(n):
    L = []
    workload(lambda x: L.insert(0, x), L.append, lambda: L.pop(0), L.pop, n)

def run_circular(n):
    D = ArrayDeque()
    workload(D.add_first, D.add_last, D.delete_first, D.delete_last, n)

def run_deque(n):
    D = collections.deque()
    workload(D.appendleft, D.append, D.popleft, D.pop, n)

for n in (5000, 20000):
    times = []
    for f in (run_list, run_circular, run_deque):
        start = time.perf_counter(); f(n); times.append(round(time.perf_counter() - start, 4))
    print("C-Q11: n =", n, "| list, circular, deque (s):", times)


# Part D, Q1 and Q3
class _Node:
    def __init__(self, element, next_node): self.element, self.next = element, next_node

class SinglyLinkedList:
    def __init__(self): self._head = self._tail = None; self._size = 0
    def __len__(self): return self._size
    def insert_first(self, e):
        self._head = _Node(e, self._head)
        if self._tail is None: self._tail = self._head
        self._size += 1
    def insert_last(self, e):
        node = _Node(e, None)
        if self._tail is None: self._head = node
        else: self._tail.next = node
        self._tail = node
        self._size += 1
    def delete_first(self):
        if self._head is None: raise Empty("List is empty")
        value, self._head = self._head.element, self._head.next
        self._size -= 1
        if self._head is None: self._tail = None
        return value
    def __iter__(self):
        walk = self._head
        while walk is not None:
            yield walk.element
            walk = walk.next

L = SinglyLinkedList()
print("D-Q3: empty", list(L))
L.insert_first("b"); print("D-Q3: singleton", list(L))
L.insert_first("a"); L.insert_last("c")
print("D-Q3: multi", list(L), "| deleted", L.delete_first(), "->", list(L))


# Part D, Q4
class _DNode:
    def __init__(self, element, prev, next_node): self.element, self.prev, self.next = element, prev, next_node

class DoublyLinkedList:
    def __init__(self):
        self._header = _DNode(None, None, None)
        self._trailer = _DNode(None, self._header, None)
        self._header.next = self._trailer
        self._size = 0
    def __len__(self): return self._size
    def _insert_between(self, e, predecessor, successor):
        new = _DNode(e, predecessor, successor)
        predecessor.next = new
        successor.prev = new
        self._size += 1
        return new
    def _delete_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self._size -= 1
        return node.element
    def insert_last(self, e): return self._insert_between(e, self._trailer.prev, self._trailer)
    def __iter__(self):
        walk = self._header.next
        while walk is not self._trailer:
            yield walk.element
            walk = walk.next

DL = DoublyLinkedList()
DL.insert_last(10); DL.insert_last(30)
mid = DL._insert_between(20, DL._header.next, DL._header.next.next)
print("D-Q4: after insert", list(DL), end=" | ")
DL._delete_node(mid)
print("after delete", list(DL))


# Part D, Q6
class FavoritesList(DoublyLinkedList):
    class _Item:
        def __init__(self, value): self.value, self.count = value, 0

    def _find(self, e):
        walk = self._header.next
        while walk is not self._trailer:
            if walk.element.value == e: return walk
            walk = walk.next

    def access(self, e):
        node = self._find(e) or self._insert_between(self._Item(e), self._trailer.prev, self._trailer)
        item = node.element
        item.count += 1
        walk = node.prev
        while walk is not self._header and walk.element.count < item.count:
            walk = walk.prev
        if walk is not node.prev:
            self._delete_node(node)
            self._insert_between(item, walk, walk.next)

    def remove(self, e):
        node = self._find(e)
        if node is None: raise ValueError("%r not in list" % (e,))
        self._delete_node(node)

    def top(self, k):
        if not 1 <= k <= len(self): raise ValueError("need 1 <= k <= %d" % len(self))
        return [item.value for item in self][:k]

F = FavoritesList()
for page in ["home", "docs", "home", "blog", "docs", "home", "blog", "blog"]:
    F.access(page)
print("D-Q6: top(2) =", F.top(2), end=" | ")
F.remove("home")
print("after remove(home), top(2) =", F.top(2))
