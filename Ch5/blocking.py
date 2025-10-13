def block_model(s):
    m = s.model()
    s.add(Or([f() != m[f] for f in m.decls() if f.arity() == 0]))

def block_model(s, terms):
    m = s.model()
    s.add(Or([t != m.eval(t, model_completion=True) for t in terms]))

# 여러 개의 해(모델)를 순차적으로 탐색
def all_smt(s, terms):
    while sat == s.check():
        print(s.model())
        block_model(s, terms)

# 여러 개의 해(모델)를 순차적으로 탐색 with scope
def all_smt(s, initial_terms):
    def block_term(s, m, t):
        s.add(t != m.eval(t, model_completion=True))
    def fix_term(s, m, t):
        s.add(t == m.eval(t, model_completion=True))
    def all_smt_rec(terms):
        if sat == s.check():
            m = s.model()
            yield m
            for i in range(len(terms)):
                s.push()
                block_term(s, m, terms[i])
                for j in range(i):
                    fix_term(s, m, terms[j])
                yield from all_smt_rec(terms[i:])
                s.pop()
    yield from all_smt_rec(list(initial_terms))
