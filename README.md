# esolangs
Esoteric Programming Languages

Stuff I make when I'm bored...

==Hanoiing - an esolang inspired by the Towers of Hanoi puzzle==
Language is unicode based and uses a single unbounded integer register, three
 unbounded stacks of unbounded integer size each of which maintain the
 invariant that each element is smaller than the one under it.

Instructions are as following:
* a, b, c: pop the top value from the corresponding stack into the register and branch if empty
* A, B, C: push the register value onto the corresponding stack and branch if invalid
**  Branching executes the next character and skips it otherwise
* =: set the register to the value represented by the following decimal digits
* +, -: increment/decrement the register
* ~: negate the register
* j: jump to the byte index, ignoring the instruction if invalid
* J: ditto, but using the register's value
* l: jump to beginning line number, ignoring the instruction if invalid
* L: ditto, but using the register's value
* z: execute the next character if the register == 0 (otherwise, skip it)
* p: ditto for positive numbers
* n: ditto for negative numbers
* i: read the next unicode point of stdin into the register
* o: output the register's unicode value to stdout
* all other characters are no-op
