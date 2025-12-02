from z3 import *

def sudoku_solver(given_grid) :
    """
    given_grid : 9x9 파이썬 리스트. 빈 칸은 0 사용.
    예: [
        [5,3,0, 0,7,0, 0,0,0],
        [6,0,0, 1,9,5, 0,0,0],
        ...
    ]
    """

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

    # 8. 해 탐색
    if s.check() == sat :
        m = s.model()
        solution = [[m.evaluate(X[i][j]).as_long() for j in range(9)]
                    for i in range(9)]
        return solution
    else :
        return None

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
    # 예시 퍼즐 (0은 빈 칸)
    puzzle = [
        [5,3,0, 0,7,0, 0,0,0],
        [6,0,0, 1,9,5, 0,0,0],
        [0,9,8, 0,0,0, 0,6,0],

        [8,0,0, 0,6,0, 0,0,3],
        [4,0,0, 8,0,3, 0,0,1],
        [7,0,0, 0,2,0, 0,0,6],

        [0,6,0, 0,0,0, 2,8,0],
        [0,0,0, 4,1,9, 0,0,5],
        [0,0,0, 0,8,0, 0,7,9],
    ]

    sol = sudoku_solver(puzzle)
    if sol is None:
        print("No solution.")
    else:
        print("Solution:")
        print_grid(sol)