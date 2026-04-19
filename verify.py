import numpy as np

def read_matrix(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    matrix = []
    for i in range(1, n + 1):
        row = list(map(float, lines[i].split()))
        matrix.append(row)
    return np.array(matrix)

a = read_matrix("matrix_a.txt")
b = read_matrix("matrix_b.txt")
c_program = read_matrix("result.txt")
c_check = a @ b

if np.allclose(c_program, c_check, atol=1e-6):
    print("Verification passed")
else:
    print("Verification failed")
    print("Program result:")
    print(c_program)
    print("NumPy result:")
    print(c_check)