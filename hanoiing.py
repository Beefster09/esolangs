#!/usr/bin/python3

# Hanoiing - an esolang inspired by the Towers of Hanoi puzzle
# Language is unicode based and uses a single unbounded integer register, three
#  unbounded stacks of unbounded integer size each of which maintain the
#  invariant that each element is smaller than the one under it.
#
# Instructions are as following
# a, b, c: pop the top value from the corresponding stack into the register and branch if empty
# A, B, C: push the register value onto the corresponding stack and branch if invalid
#   Branching executes the next character and skips it otherwise
# =: set the register to the value represented by the following decimal digits
# +, -: increment/decrement the register
# ~: negate the register
# j: jump to the byte index ___, ignoring the instruction if invalid
# J: ditto, but using the register's value
# l: jump to beginning line number ___, ignoring the instruction if invalid
# L: ditto, but using the register's value
# z: execute the next character if the register == 0 (otherwise, skip it)
# p: ditto for positive numbers
# n: ditto for negative numbers
# i: read the next unicode point of stdin into the register
# o: output the register's unicode value to stdout
# all other bytes are no-op

import functools
import re
import sys

DECIMAL = re.compile(r"\d+")

def get_line_indices(s):
    yield 0
    idx = 0
    while True:
        idx = s.find('\n', idx) + 1
        yield idx
        if idx == 0:
            break

def execute(prog, debug=False):
    assert isinstance(prog, str)

    lines = list(get_line_indices(prog))

    pc = 0
    reg = 0
    stackA = []
    stackB = []
    stackC = []

    def push(stack):
        nonlocal pc, reg
        if len(stack) == 0 or reg < stack[-1]:
            stack.append(reg)
            pc += 1 # successful; skip next byte

    def pop(stack):
        nonlocal pc, reg
        if len(stack) > 0:
            reg = stack.pop()
            pc += 1 # successful; skip next byte

    def get_number():
        nonlocal pc
        match = DECIMAL.match(prog[pc:])
        if match:
            num = match.group(0)
            pc += len(num)
            return int(num, 10)
        else:
            return 0

    def setreg():
        nonlocal pc, reg
        reg = get_number()

    def inc():
        nonlocal reg
        reg += 1

    def dec():
        nonlocal reg
        reg -= 1

    def neg():
        nonlocal reg
        reg = -reg

    def jump():
        nonlocal pc
        num = get_number()
        if num >= 0 and num < len(prog):
            pc = num

    def jump_reg():
        nonlocal pc, reg
        if reg >= 0 and reg < len(prog):
            pc = reg

    def jump_line():
        nonlocal pc
        line = get_number()
        if line >= 1 and line <= len(lines):
            pc = lines[line - 1]

    def jump_lr():
        nonlocal pc
        if reg >= 1 and reg <= len(lines):
            pc = lines[reg - 1]

    def ifzero():
        nonlocal pc, reg
        if reg != 0:
            pc += 1

    def ifneg():
        nonlocal pc, reg
        if reg >= 0:
            pc += 1

    def ifpos():
        nonlocal pc, reg
        if reg <= 0:
            pc += 1

    def read():
        nonlocal reg
        reg = ord(sys.stdin.read(1))

    def write():
        nonlocal reg
        sys.stdout.write(chr(reg % 0x110000))

    opcodes = {
        'a': functools.partial(pop, stackA),
        'b': functools.partial(pop, stackB),
        'c': functools.partial(pop, stackC),
        'A': functools.partial(push, stackA),
        'B': functools.partial(push, stackB),
        'C': functools.partial(push, stackC),
        '=': setreg,
        '+': inc,
        '-': dec,
        '~': neg,
        'j': jump,
        'J': jump_reg,
        'l': jump_line,
        'z': ifzero,
        'n': ifneg,
        'p': ifpos,
        'i': read,
        'o': write
    }

    while pc < len(prog):
        instruction = opcodes.get(prog[pc], lambda: None)
        if debug:
            print()
            print("PC: {} '{}'".format(pc, prog[pc]))
            print("Register:", reg)
            print("Stacks:")
            print(stackA)
            print(stackB)
            print(stackC)
        pc += 1
        instruction()

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        execute(f.read(), len(sys.argv) > 2 and sys.argv[2] == 'debug')
