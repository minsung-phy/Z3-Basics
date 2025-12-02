from z3 import *

def check_uniqueness(given_grid) :
    # assert로 입력의 형태가 진짜 9x9인지 체크 (조건이 False면 프로그램이 바로 죽음)
    assert len(given_grid) == 9 and all(len(row) == 9 for row in given_grid)

    # 1. 변수 선언 : 9x9 Int 변수 (1~9)
    X = [[Int(f"x_{i}_{j}") for j in range(9)] for i in range(9)]

    # 2. 각 칸은 1~9 범위
    cell_constraints = [
        And(1 <= X[i][j], X[i][j] <= 9)
        for i in range(9) for j in range(9)
    ]

    # 3. 각 행은 모두 서로 다른 값
    row_constraints = [
        Distinct(X[i]) for i in range(9)
    ]

    # 4. 각 열도 모두 서로 다른 값
    col_constraints = [
        Distinct([X[i][j] for i in range(9)]) for j in range(9)
    ]

    # 5. 각 3x3 블록도 모두 서로 다른 값
    block_constraints = []
    for bi in range(3) :
        for bj in range(3) :
            block = [
                X[3*bi + di][3*bj + dj]
                for di in range(3)
                for dj in range(3)
            ]
            block_constraints.append(Distinct(block))

    # 6. 주어진 숫자(힌트) 반영
    given_constraints = []
    for i in range(9) :
        for j in range(9) :
            if given_grid[i][j] != 0 :
                given_constraints.append(X[i][j] == given_grid[i][j])
    
    # 7. Solver에 모두 추가
    s = Solver()
    s.add(cell_constraints + row_constraints + col_constraints + block_constraints + given_constraints)

    # 8. 첫 번째 해 구하기
    if s.check() != sat :
        return "no-solution", None

    m1 = s.model()
    sol1 = [[m1.evaluate(X[i][j]).as_long() for j in range(9)] for i in range(9)]
    
    # 9. 첫 번째 해와 다른 해를 강제하는 제약 추가
    diff_clause = Or([
        X[i][j] != sol1[i][j]
        for i in range(9) for j in range(9)
    ])
    s.add(diff_clause)

    # 10. 다시 check
    if s.check() == sat :
        # 또 다른 해가 존재 -> multiple
        m2 = s.model()
        sol2 = [[m2.evaluate(X[i][j]).as_long() for j in range(9)]
                for i in range(9)]
        return "multiple", (sol1, sol2)
    else :
        # 유일 해
        return "unique", sol1

def print_grid(grid) :
    for i, row in enumerate(grid) :
        line = ""
        for j, v in enumerate(row) :
            line += str(v) + " "
            if j % 3 == 2 and j != 8 :
                line += "| "
        print(line)
        if i % 3 == 2 and i != 8 :
            print("-" * 21)

if __name__ == "__main__" :
    puzzle = [
        # 여러 해
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0],

        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0],

        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0]
        
    ]

    ''' 유일해 :
        [5,3,0, 0,7,0, 0,0,0],
        [6,0,0, 1,9,5, 0,0,0],
        [0,9,8, 0,0,0, 0,6,0],

        [8,0,0, 0,6,0, 0,0,3],
        [4,0,0, 8,0,3, 0,0,1],
        [7,0,0, 0,2,0, 0,0,6],

        [0,6,0, 0,0,0, 2,8,0],
        [0,0,0, 4,1,9, 0,0,5],
        [0,0,0, 0,8,0, 0,7,9]
    '''

    '''
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0],

        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0],

        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0],
        [0,0,0, 0,0,0, 0,0,0]
    '''

    kind, result = check_uniqueness(puzzle)
    if kind == "no-solution" :
        print("해가 존재하지 않습니다.")
    elif kind == "unique" :
        print("유일해입니다.")
        print_grid(result)
    else :
        print("해가 여러 개 있습니다.")
        sol1, sol2 = result
        print("첫 번째 해:")
        print_grid(sol1)
        print("\n두 번째 해:")
        print_grid(sol2)