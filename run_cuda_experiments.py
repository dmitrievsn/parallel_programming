import numpy as np
import subprocess
import re
import csv

def write_matrix(filename, matrix):
    n = matrix.shape[0]
    with open(filename, "w") as f:
        f.write(f"{n}\n")
        for row in matrix:
            f.write(" ".join(f"{x:.6f}" for x in row) + "\n")

def generate_matrices(n):
    a = np.random.rand(n, n) * 10
    b = np.random.rand(n, n) * 10
    write_matrix("matrix_a.txt", a)
    write_matrix("matrix_b.txt", b)

sizes = [200, 400, 800, 1200, 1600, 2000]
blocks = [8, 16, 32]

results = []

for n in sizes:
    print(f"\n=== SIZE {n} ===")
    generate_matrices(n)

    for b in blocks:
        print(f"Running block {b}x{b}")

        result = subprocess.run(
            ["matrix_mul_cuda.exe", str(b)],
            capture_output=True,
            text=True
        )

        output = result.stdout

        match = re.search(r"Execution time \(ms\): ([\d.]+)", output)
        if match:
            time_ms = float(match.group(1))
        else:
            time_ms = -1

        print(f"time: {time_ms} ms")

        results.append({
            "size": n,
            "block": b,
            "time_ms": time_ms
        })

with open("cuda_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["size", "block", "time_ms"])
    writer.writeheader()
    writer.writerows(results)

print("\nDone. Results saved to cuda_results.csv")