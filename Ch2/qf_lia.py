# SMT-LIB 예시 코드
# (set-logic QF_LIA)
# (declare-const x Int)
# (declare-const y Int)
# (assert (> (+ (mod x 4) (* 3 (div y 2))) (- x y)))
# (check-sat)

# Python 버전
from z3 import *
x, y = Ints('x y')
s = Solver()
s.add((x % 4) + 3 * (y / 2) > x - y)

print(s.sexpr()) # Solver 상태를 SMT-LIB2 형식으로 출력하기