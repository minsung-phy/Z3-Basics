from z3 import *
Tie, Shirt = Bools('Tie Shirt')  # 불리언(참/거짓) 변수 2개 생성
s = Solver()                     # 문제 해결기(Solver) 만들기

# 조건 3개 추가
s.add(Or(Tie, Shirt))            # Tie 또는 Shirt 중 하나는 참
s.add(Or(Not(Tie), Shirt))       # Tie가 아니면 Shirt는 참
s.add(Or(Not(Tie), Not(Shirt)))  # Tie가 아니면 Shirt는 거짓

print(s.check())   # 조건이 동시에 가능한지 확인
print(s.model())   # 가능하다면, 어떤 값일 때 가능한지 보여줌