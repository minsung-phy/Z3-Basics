def tt(s, f):
    return is_true(s.model().eval(f))

def get_mss(s, ps):
    if sat != s.check():
        return []
    mss = { q for q in ps if tt(s, q) }
    return get_mss(s, mss, ps)

def get_mss(s, mss, ps):
    ps = ps - mss
    backbones = set([])
    while len(ps) > 0:
        p = ps.pop()
        if sat == s.check(mss | backbones | {p}):
            # p를 추가해도 만족된다면 MSS에 추가
            mss = mss | {p} | {q for q in ps if tt(s, q)}
            ps = ps - mss
        else:
            # 추가 시 모순이라면 backbone(항상 참/거짓으로 고정된 식)에 기록
            backbones = backbones | {Not(p)}
    return mss