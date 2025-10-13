class BlockTracked(UserPropagateBase):
    def __init__(self, s):
        UserPropagateBase.__init__(self, s)
        self.trail = []   # 현재까지의 변수 할당 기록
        self.lim = []     # push/pop을 위한 경계 스택

        # Boolean 또는 BitVec 값이 할당(fixed)될 때 호출되는 콜백 등록
        self.add_fixed(lambda x, v: self._fixed(x, v))

        # 모델이 완성(모든 변수 할당 완료)되었을 때 호출되는 콜백 등록
        self.add_final(lambda: self._final())

    def push(self):
        self.lim += [len(self.trail)]

    def pop(self, n):
        self.trail = self.trail[:self.lim[len(self.lim) - n]]
        self.lim = self.lim[:len(self.lim) - n]

    def _fixed(self, x, v):
        # 변수 x에 값 v가 할당되면 trail에 추가
        self.trail += [(x, v)]

    def _final(self):
        # 모든 변수의 할당이 완료되었을 때 실행
        print(self.trail)
        self.conflict([x for x, v in self.trail])  # 현재 조합을 차단

# 예제 실행
s = SimpleSolver()
b = BlockTracked(s)

x, y, z, u = Bools('x y z u')
b.add(x)
b.add(y)
b.add(z)

s.add(Or(x, Not(y)), Or(z, u), Or(Not(z), x))
print(s.check())