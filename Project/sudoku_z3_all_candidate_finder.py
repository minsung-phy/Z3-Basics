from z3 import *

def build_sudoku_solver(given_grid) :
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

    return s, X

def all_candidates(given_grid) :
    """
    각 칸의 후보 리스트를 9x9 구조로 반환.
    - 빈 칸(0)이면 : 가능한 값 리스트 (예: [1, 3, 9])
    - 이미 숫자가 있는 칸이면 : [그 숫자 하나]
    """
    s, X = build_sudoku_solver(given_grid)

    # 퍼즐 자체가 모순이면 후보 개념이 의미가 없으니 빈 리스트 반환
    if s.check() != sat :
        return None
    
    candidates = [[[] for _ in range(9)] for _ in range(9)]

    for i in range(9) :
        for j in range(9) :
            if given_grid[i][j] != 0 :
                # 이미 값이 있는 칸 -> 그 값만 후보로 취급
                candidates[i][j] = [given_grid[i][j]]
                continue
            
            cell_cands = []
            for k in range(1, 10) :
                s.push()
                s.add(X[i][j] == k)
                if s.check() == sat :
                    cell_cands.append(k)
                s.pop()
            candidates[i][j] = cell_cands
        
    return candidates

def print_candidates(cands):
    CELL_WIDTH = 11   # 칸 하나의 고정 폭

    for i in range(9):
        line = ""
        for j in range(9):
            vals = cands[i][j]

            # 후보 형식: {1,3,5} 또는 "7"
            if len(vals) == 1:
                text = str(vals[0])
            else:
                text = "{" + ",".join(str(v) for v in vals) + "}"

            # 고정 폭에 가운데 정렬
            line += text.center(CELL_WIDTH)

            # 블록 구분선
            if j % 3 == 2 and j != 8:
                line += "|"

        print(line)

        # 가로 블록 구분선
        if i % 3 == 2 and i != 8:
            print("-" * (CELL_WIDTH * 3 + 2))


if __name__ == "__main__" :
    puzzle = [
        [0,0,0, 0,0,0, 0,0,0],
        [6,0,0, 1,9,5, 0,0,0],
        [0,9,8, 0,0,0, 0,6,0],

        [8,0,0, 0,6,0, 0,0,3],
        [4,0,0, 8,0,3, 0,0,1],
        [7,0,0, 0,2,0, 0,0,6],

        [0,6,0, 0,0,0, 2,8,0],
        [0,0,0, 4,1,9, 0,0,5],
        [0,0,0, 0,8,0, 0,7,9]
    ]

    # (0,2)칸에 들어갈 수 있는 후보
    cands = all_candidates(puzzle)
    if cands is None :
            print("퍼즐 자체가 모순입니다.")
    else :
        print("Candidate table :")
        print_candidates(cands)