def addr(a, b, c, r):
    r[c] = r[a] + r[b]

def addi(a, b, c, r):
    r[c] = r[a] + b

def mulr(a, b, c, r):
    r[c] = r[a] * r[b]

def muli(a, b, c, r):
    r[c] = r[a] * b

def banr(a, b, c, r):
    r[c] = r[a] & r[b]

def bani(a, b, c, r):
    r[c] = r[a] & b

def borr(a, b, c, r):
    r[c] = r[a] | r[b]

def bori(a, b, c, r):
    r[c] = r[a] | b

def setr(a, b, c, r):
    r[c] = r[a]

def seti(a, b, c, r):
    r[c] = a

def gtir(a, b, c, r):
    r[c] = 1 if a > r[b] else 0

def gtri(a, b, c, r):
    r[c] = 1 if r[a] > b else 0

def gtrr(a, b, c, r):
    r[c] = 1 if r[a] > r[b] else 0

def eqir(a, b, c, r):
    r[c] = 1 if a == r[b] else 0

def eqri(a, b, c, r):
    r[c] = 1 if r[a] == b else 0

def eqrr(a, b, c, r):
    r[c] = 1 if r[a] == r[b] else 0

opcodes = [setr, eqrr, gtri, muli, eqir, borr, bori, mulr, gtrr, seti, banr, eqri, addr, gtir, addi, bani]