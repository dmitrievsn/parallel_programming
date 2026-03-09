import random
import subprocess
import sys

sizes = [200, 400, 800, 1200, 1600, 2000]
threads_list = [1, 2, 4, 8]

with open("results_table.txt", "w", encoding="utf-8") as table:
    table.write("Size\tThreads\tTime(ms)\tVolume\tVerification\n")

    for n in sizes:
        with open("matrix_a.txt", "w", encoding="utf-8") as f:
            f.write(str(n) + "\n")
            for i in range(n):
                row = [str(random.randint(1, 9)) for j in range(n)]
                f.write(" ".join(row) + "\n")

        with open("matrix_b.txt", "w", encoding="utf-8") as f:
            f.write(str(n) + "\n")
            for i in range(n):
                row = [str(random.randint(1, 9)) for j in range(n)]
                f.write(" ".join(row) + "\n")

        for threads in threads_list:
            run_program = subprocess.run(
                [".\\matrix_mul.exe", str(threads)],
                capture_output=True,
                text=True
            )

            run_verify = subprocess.run(
                [sys.executable, "verify.py"],
                capture_output=True,
                text=True
            )

            time_value = ""
            volume_value = ""

            for line in run_program.stdout.splitlines():
                if "Execution time" in line:
                    time_value = line.split(":", 1)[1].strip()
                if "Task volume" in line:
                    volume_value = line.split(":", 1)[1].strip()

            verification = run_verify.stdout.strip()

            table.write(f"{n}x{n}\t{threads}\t{time_value}\t{volume_value}\t{verification}\n")

            print(f"{n}x{n}, threads={threads}")
            print(run_program.stdout.strip())
            print(verification)
            print()

print("Done")
print("results_table.txt updated")