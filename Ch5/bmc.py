index = 0
def fresh(s):
    global index
    index += 1
    return Const("!f%d" % index, s)

def zipp(xs, ys):
    return [p for p in zip(xs, ys)]

def bmc(init, trans, goal, fvs, xs, xns):
    s = Solver()
    s.add(init)
    count = 0
    while True:
        print("iteration ", count)
        count += 1
        p = fresh(BoolSort())
        s.add(Implies(p, goal))
        if sat == s.check(p):
            print(s.model())
            return
        s.add(trans)
        ys = [fresh(x.sort()) for x in xs]
        nfvs = [fresh(x.sort()) for x in fvs]
        trans = substitute(trans,
                           zipp(xns + xs + fvs, ys + xns + nfvs))
        goal = substitute(goal, zipp(xs, xns))
        xs, xns, fvs = xns, ys, nfvs