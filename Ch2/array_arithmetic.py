from z3 import *

Z = IntSort()                         # 정수형 정렬(Int sort)
f = Function('f', Z, Z)               # 정수 -> 정수 함수 f
x, y, z = Ints('x y z')               # 정수 변수 3개 선언
A = Array('A', Z, Z)                  # 정수 인덱스, 정수 값 배열 A

fml = Implies(x + 2 == y, f(Store(A, x, 3)[y - 2]) == f(y - x + 1))
solve(Not(fml))