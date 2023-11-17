
import random
import copy


class Clause:
    def __init__(self, p, n):
        self.p = set(p)
        self.n = set(n)

    def __str__(self):
        return "p: " + str(self.p) + ", n: " + str(self.n)

    def __repr__(self):
        return "p: " + str(self.p) + ", n: " + str(self.n)

    def __hash__(self):
        # freezes a set so it doesnt change,
        # remains the same, frozensets can be used as keys
        return hash((frozenset(self.p), frozenset(self.n)))

      # equal between two hash values
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.p == other.p and self.n == other.n

    def is_subset(self, other):

        return self.p.issubset(other.p) and self.n.issubset(other.n)
        '''if len(self.p) > len(other.p) or len(self.n) > len(other.n):
            return False
        if self.p <= other.p and self.n <= other.n:
            return True'''

        return False

    def is_strict_subset(self, other):
        if not self.is_subset(other):
            return False
        if self.p < other.p or self.n < other.n:
            return True
        return False


def resolution(A, B):  # A: clause, B: clause
    # print('A = ', A, ', B = ', B)

    A_copy = copy.deepcopy(A)
    B_copy = copy.deepcopy(B)

    if not (A_copy.p.intersection(B_copy.n)) and not (A_copy.n.intersection(B.p)):
        return False  # There is no solution (no intersection)

    if (A_copy.p.intersection(B_copy.n)):
        a = random.choice(list(A_copy.p.intersection(B_copy.n)))
        # Removes element a from the set if its in the intersection
        A_copy.p.remove(a)
        B_copy.n.remove(a)
    else:
        a = random.choice(list(A.n.intersection(B.p)))
        A_copy.n.remove(a)
        B_copy.p.remove(a)

    C = Clause(p=set(A_copy.p).union(B_copy.p),
               n=set(A_copy.n).union(B_copy.n))
    # C.p.add(A.p.union(B.p)) # Adds the union
    # C.n.add(A.n.union(B.n))
    if C.p.intersection(C.n):  # C is tautology(always true)
        return False

    # C is a set so it should not have any duplicates by default
    return C  # Returns resolvent of A & B or false


def solver(KB):

    print('Första gångeeeeeeeeen: ')
    for C in KB:
        print(' ', C)

    while True:

        S = set()
        # KB_copy = copy.deepcopy(KB)
        KB_prim = copy.deepcopy(KB)

        # print('KB: ', KB)

        # for A,B in enumerate(KB):
        my_list = list(KB)

        for i in range(len(KB)-1):
            for j in range(i+1, len(KB)):
                C = resolution(my_list[i], my_list[j])
                if C is not False:
                    S = S | set({C})

        if not S:
            return KB

        KB = incorporate(S, KB)

        print('S: ')
        for C in S:
            print(' ', C)

        print('KB: ')
        for C in KB:
            print(' ', C)

        print()

        if KB_prim == KB:
            break

    return KB


def incorporate(S, KB):  # S: set of clauses, KB: set of clauses
    for A in copy.deepcopy(S):
        KB = incorporate_clause(A, KB)
        print("incoperate clause")
    return KB


def incorporate_clause(A, KB):  # A: clause, KB: Set of clauses
    for B in copy.deepcopy(KB):
        if B.is_subset(A):
            return KB

    for B in copy.deepcopy(KB):
        if A.is_subset(B):
            KB.remove(B)

    KB = KB.union(set({A}))
    return KB


# Example 1 - Resolution
# 1.
A1 = Clause(p={'a', 'b'}, n={'c'})
B1 = Clause(p={'c', 'b'}, n={})
result1 = resolution(A1, B1)
print('Ex 1: ', result1)

# 2.
A2 = Clause(p={'a', 'b'}, n={'c'})
B2 = Clause(p={'d', 'b'}, n={'g'})
result2 = resolution(A2, B2)
print('Ex 2: ', result2)

# 3.
A3 = Clause(p={'c', 't'}, n={'b'})
B3 = Clause(p={'z', 'b'}, n={'c'})
result3 = resolution(A3, B3)
print('Ex 3: ', result3)

# Subsumption
# 1.
A5 = Clause(p={'c', 'a'}, n={})
B5 = Clause(p={'a', 'b', 'c'}, n={})
result5 = A5.is_strict_subset(B5)
print('Strict subset 1: ', result5)

# 2.
A5 = Clause(p={'b'}, n={'c'})
B5 = Clause(p={'a', 'b'}, n={'c'})
result5 = A5.is_strict_subset(B5)
print('Strict subset 2: ', result5)

# 3.
A5 = Clause(p={'b'}, n={'f', 'c'})
B5 = Clause(p={'a', 'b'}, n={'c'})
result5 = A5.is_strict_subset(B5)
print('Strict subset 3: ', result5)

# 4.
A5 = Clause(p={'b'}, n={})
B5 = Clause(p={'a', 'b'}, n={'c'})
result5 = A5.is_strict_subset(B5)
print('Strict subset 4: ', result5)

# 5.
A5 = Clause(p={'b', 'a'}, n={'c'})
B5 = Clause(p={'a', 'b'}, n={'c'})
result5 = A5.is_strict_subset(B5)
result6 = A5.is_subset(B5)
print('Strict Subset 5: ', result5)

print('\nBob\n')
# Drawing conclusion
# Bob.
ice = 'a'
sun = 'b'
money = 'c'
movie = 'd'
cry = 'e'
A4 = Clause(p={'ice'}, n={'sun', 'money'})
B4 = Clause(p={'ice', 'movie'}, n={'money'})
C4 = Clause(p={'money'}, n={'movie'})
D4 = Clause(p={}, n={'movie', 'ice'})
E4 = Clause(p={'sun', 'money', 'cry'}, n={})
F4 = Clause(p={'movie'}, n={})

KB = set({A4, B4, C4, D4, E4, F4})
KB1 = incorporate(S={}, KB=KB)  # To remove B4 as a clauses
result4 = solver(KB1)
print('KB: ', result4)
print('\nFinal Clauses: ')
for C in result4:
    print(C)


print('\nIs A suspicious?\n')
# Task B - Robbery puzzle
A5 = Clause(p={'a', 'b', 'c'}, n={})
B5 = Clause(p={'a'}, n={'c'})
C5 = Clause(p={'a', 'c'}, n={'b'})

# a V b V c
# c -> a        =   -c V a
# b -> c V a    =   -b V c V a

KB = set({A5, B5, C5})
result5 = solver(KB)
print('\nFinal Clauses: ')
for C in result5:
    print(C)
