import subprocess
import numpy as np
import csv
import re

SIZES = [200, 400, 800, 1200, 1600, 2000]
PROCESSES = [1, 2, 4, 8]

def write_matrix(filename, matrix):
    n = matrix.shape[0]
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{n}\n")
        for row in matrix:
            f.write(" ".join(f"{x:.6f}" for x in row) + "\n")

def generate_matrices(n):
    a = np.random.rand(n, n) * 10
    b = np.random.rand(n, n) * 10
    write_matrix("matrix_a.txt", a)
    write_matrix("matrix_b.txt", b)

def run_program(proc_count):
    if proc_count <= 2:
        cmd = ["mpirun", "-np", str(proc_count), "./mpi_matrix_mult"]
    else:
        cmd = ["mpirun", "--oversubscribe", "-np", str(proc_count), "./mpi_matrix_mult"]

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + "\n" + result.stderr

    match = re.search(r"Execution time \(ms\):\s*([0-9.]+)", output)
    if match:
        return float(match.group(1)), output
    return None, output

def main():
    rows = []

    for n in SIZES:
        print(f"\n=== Matrix size: {n}x{n} ===")
        generate_matrices(n)

        for p in PROCESSES:
            print(f"Running with {p} processes...")
            time_ms, output = run_program(p)

            if time_ms is None:
                print("Failed to parse execution time")
                print(output)
                rows.append([n, p, "ERROR"])
            else:
                print(f"Time: {time_ms} ms")
                rows.append([n, p, time_ms])

    with open("results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["matrix_size", "processes", "time_ms"])
        writer.writerows(rows)

    print("\nDone. Results saved to results.csv")

if __name__ == "__main__":
    main()
