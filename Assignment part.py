import math, platform, random, statistics, sys, time
import matplotlib
matplotlib.use("Agg")                      # save plots to files
import matplotlib.pyplot as plt

random.seed(1)
print("Python", sys.version.split()[0], "|", platform.platform(),
      "| times are MEDIANS of 5 trials")


def timeit(f, *args, number=1, repeats=5):
    """Median time (s) of one call; data is built by the caller, outside."""
    trials = []
    for _ in range(repeats):
        t = time.perf_counter()
        for _ in range(number):
            f(*args)
        trials.append((time.perf_counter() - t) / number)
    return statistics.median(trials)


def slope(ns, ts):
    """Log-log slope = measured exponent k in T ~ n^k."""
    x = [math.log(n) for n in ns]; y = [math.log(t) for t in ts]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)

# Part 3, Question 1:
# "Analyse a loop that repeatedly replaces n by floor(n/2) until n<=1.
#  Derive the iteration count and asymptotic complexity."
print("\n--- Part 3.1: loop n = n // 2 until n <= 1 ---")
def halving(n):
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return count

for n in [1, 2, 7, 8, 1000, 10**6]:
    print("n =", n, "-> iterations =", halving(n), "| floor(log2 n) =", int(math.log2(n)))
assert all(halving(n) == n.bit_length() - 1 for n in range(1, 100000))
print("Iterations = floor(log2 n)  ->  Theta(log n)")

# Part 3, Question 2:
# "Compare direct prefix-average computation that recomputes each prefix
#  sum with an implementation that maintains a running sum. Derive both
#  time complexities."

def prefix_average1(S):                    # quadratic: recompute each sum
    A = []
    for j in range(len(S)):
        total = 0
        for i in range(j + 1):
            total += S[i]
        A.append(total / (j + 1))
    return A

# Lab Work (Prefix Averages), Task 2:
# "Implement prefix_average2 using a running sum updated once for each
#  new element."
def prefix_average2(S):                    # linear: running sum
    A, total = [], 0
    for j, x in enumerate(S):
        total += x
        A.append(total / (j + 1))
    return A

# Part 3, Question 2 (continued): number of additions for each method
print("\n--- Part 3.2: prefix averages, additions performed ---")
for n in [10, 100, 1000]:
    print("n =", n, "| method 1:", n * (n + 1) // 2, "(n(n+1)/2) | method 2:", n)

# Part 3, Question 3:
# "Compare the three element-uniqueness methods in asymptotic complexity,
#  practical considerations and memory use."
def unique1(S):                            # O(n^2) time, O(1) space
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            if S[i] == S[j]:
                return False
    return True

def unique2(S):                            # O(n log n) time, O(n) space (copy)
    T = sorted(S)
    return all(T[i] != T[i + 1] for i in range(len(T) - 1))

def unique3(S):                            # O(n) expected time, O(n) space
    return len(set(S)) == len(S)

print("\n--- Part 3.3: element uniqueness (worst case: all distinct), ms ---")
print("%6s %12s %12s %12s" % ("n", "O(n^2)", "O(n log n)", "O(n) set"))
for n in [250, 500, 1000, 2000]:
    data = random.sample(range(10 * n), n)
    assert unique1(data) and unique2(data) and unique3(data)
    data[-1] = data[0]
    assert not unique1(data) and not unique2(data) and not unique3(data)
    data = random.sample(range(10 * n), n)
    print("%6d %12.3f %12.3f %12.3f" % (n, *[timeit(f, data) * 1e3 for f in (unique1, unique2, unique3)]))

# Lab Work 1: Benchmarking Algorithmic Growth Rates
# Objective: "Empirically investigate constant, logarithmic, linear,
#             nlogn, quadratic and exponential growth patterns."
#
# Task 1: "Implement representative operations/algorithms: list indexing,
#          binary search, linear search, merge sort, a double-loop pair
#          counter and (for small n only) exponential subset enumeration."
#          -> the six functions below.
def list_index(a, i): return a[i]

def linear_search(a, x):
    for i, v in enumerate(a):
        if v == x:
            return i
    return -1

def binary_search(a, x):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x: return mid
        if a[mid] < x: lo = mid + 1
        else: hi = mid - 1
    return -1

def merge_sort(a):
    if len(a) <= 1:
        return a
    m = len(a) // 2
    l, r, out, i, j = merge_sort(a[:m]), merge_sort(a[m:]), [], 0, 0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]: out.append(l[i]); i += 1
        else: out.append(r[j]); j += 1
    return out + l[i:] + r[j:]

def count_pairs(a, target):                # double loop
    c = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] + a[j] == target:
                c += 1
    return c

def subsets(n):                            # visits all 2^n subsets
    def rec(i):
        return 1 if i == n else rec(i + 1) + rec(i + 1)
    return rec(0)

# (Correctness check of every implementation before timing it.)
s = sorted(random.sample(range(1000), 100))
assert binary_search(s, s[40]) == 40 and binary_search(s, -1) == -1
assert linear_search(s, s[40]) == 40 and linear_search(s, -1) == -1
u = random.sample(range(1000), 200)
assert merge_sort(u) == sorted(u) and count_pairs([1, 2, 3, 4], 5) == 2
assert subsets(10) == 2 ** 10

# Task 2: "Choose safe input-size ranges appropriate to each growth class;
#          exponential algorithms must use much smaller n."
# Task 3: "Repeat measurements. Exclude data generation from the timed
#          region and document input characteristics."
tests = [
    ("list indexing", "O(1)", [10**3, 10**4, 10**5, 10**6],
     lambda n: (list_index, (list(range(n)), n // 2), 100000), lambda n: 1),
    ("binary search", "O(log n)", [10**3, 10**4, 10**5, 10**6],
     lambda n: (binary_search, (list(range(n)), -1), 10000), lambda n: math.log2(n)),
    ("linear search", "O(n)", [10**3, 10**4, 10**5, 10**6],
     lambda n: (linear_search, (list(range(n)), -1), 1), lambda n: n),
    ("merge sort", "O(n log n)", [1000, 2000, 4000, 8000, 16000, 32000],
     lambda n: (merge_sort, (random.sample(range(10 * n), n),), 1), lambda n: n * math.log2(n)),
    ("double-loop pairs", "O(n^2)", [100, 200, 400, 800, 1600],
     lambda n: (count_pairs, ([random.randint(0, 99) for _ in range(n)], 100), 1), lambda n: n ** 2),
    ("subsets", "O(2^n)", [10, 12, 14, 16, 18],
     lambda n: (subsets, (n,), 1), lambda n: 2 ** n),
]

# Task 4: "Plot execution time against n. Where useful, examine normalized
#          quantities such as T(n)/n, T(n)/(nlog2n) and T(n)/n^2."
#          -> top row of the figure: T(n) versus n;
#             bottom row: T(n)/g(n) (flat curve = matches the growth class).
# Task 5: "Prepare a table of algorithm, theoretical bound, measured trend
#          and experimental limitations."
#          -> table printed at the end of this section.
print("\n--- Lab Work 1: benchmarking growth rates ---")
fig, axes = plt.subplots(2, len(tests), figsize=(20, 6))
print("%-18s %-11s %s" % ("algorithm", "theory", "measured trend"))
for k, (name, theory, sizes, build, norm) in enumerate(tests):
    times = []
    for n in sizes:
        f, args, number = build(n)         # data generation is NOT timed
        times.append(timeit(f, *args, number=number))
    print("\n%s  (n, time s, time/g(n))" % name)
    for n, t in zip(sizes, times):
        print("  %8d %12.3e %12.3e" % (n, t, t / norm(n)))
    if name == "subsets":
        trend = "x%.2f per +1 in n" % ((times[-1] / times[0]) ** (1 / (sizes[-1] - sizes[0])))
    else:
        trend = "log-log slope %.2f" % slope(sizes, times)
    axes[0][k].plot(sizes, times, "o-"); axes[0][k].set_title(name + " " + theory)
    axes[1][k].plot(sizes, [t / norm(n) for n, t in zip(sizes, times)], "s-r")
    axes[1][k].set_title("T(n)/g(n)  (flat = matches)")
    axes[0][k].set_yscale("log"); axes[0][k].set_xscale("log" if name != "subsets" else "linear")
    axes[1][k].set_ylim(bottom=0)
    tests[k] = (name, theory, trend)

print("\n%-18s %-11s %s" % ("algorithm", "theory", "measured trend"))
for name, theory, trend in tests:
    print("%-18s %-11s %s" % (name, theory, trend))
fig.tight_layout(); fig.savefig("lab1_growth_rates.png", dpi=120)
print("plot saved: lab1_growth_rates.png")


# Lab Work: Prefix Averages: Quadratic versus Linear-Time Design
# Objective: "Demonstrate the reduction from quadratic to linear time
#             using a running-sum strategy."
#
# Task 1 and Task 2: prefix_average1 and prefix_average2 are implemented
#          above (Part 3, Question 2).
print("\n--- Lab: prefix_average1 vs prefix_average2 ---")
# Task 3: "Verify equivalent outputs for singleton, positive, negative and
#          mixed-value sequences; document empty-input handling."
cases = {"empty": [], "singleton": [5], "positive": [1, 2, 3, 4],
         "negative": [-2, -4, -6], "mixed": [3, -1, 4, -1, 5, -9]}
for name, S in cases.items():
    a1, a2 = prefix_average1(S), prefix_average2(S)
    assert a1 == a2 and len(a1) == len(S)
    print("%-10s %-22s -> %s" % (name, S, a2))
print("Empty input returns [] (no error).")

# Task 4: "Benchmark both implementations for increasing sequence lengths
#          and repeat trials."
sizes = [50, 100, 200, 400, 800, 1600]
t1, t2 = [], []
print("\n%6s %14s %14s" % ("n", "average1 (s)", "average2 (s)"))
for n in sizes:
    data = [random.randint(-1000, 1000) for _ in range(n)]
    t1.append(timeit(prefix_average1, data)); t2.append(timeit(prefix_average2, data, number=20))
    print("%6d %14.3e %14.3e" % (n, t1[-1], t2[-1]))
print("slopes: average1 = %.2f (expect ~2), average2 = %.2f (expect ~1)" % (slope(sizes, t1), slope(sizes, t2)))

# Task 5: "Plot execution time versus n and compare the trends with O(n^2)
#          and O(n)."
plt.figure(figsize=(6, 4))
plt.loglog(sizes, t1, "o-", label="prefix_average1  O(n^2)")
plt.loglog(sizes, t2, "s-", label="prefix_average2  O(n)")
plt.xlabel("n"); plt.ylabel("time (s)"); plt.legend(); plt.grid(alpha=0.3)
plt.savefig("lab2_prefix_average.png", dpi=120, bbox_inches="tight")
print("plot saved: lab2_prefix_average.png")
