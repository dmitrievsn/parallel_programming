import os
import matplotlib.pyplot as plt

sizes = [200, 400, 800, 1200, 1600, 2000]

times_1 = [85.0978, 696.651, 6650.52, 23259.7, 72975.6, 140235.0]
times_2 = [42.148, 407.199, 3376.52, 11785.0, 38486.1, 77005.4]
times_4 = [29.3883, 241.975, 2008.44, 7345.57, 23687.2, 45040.4]

speedup_2 = [t1 / t2 for t1, t2 in zip(times_1, times_2)]
speedup_4 = [t1 / t4 for t1, t4 in zip(times_1, times_4)]

os.makedirs("images", exist_ok=True)

plt.figure(figsize=(10, 6))
plt.plot(sizes, times_1, marker='o', label='1 процесс')
plt.plot(sizes, times_2, marker='o', label='2 процесса')
plt.plot(sizes, times_4, marker='o', label='4 процесса')
plt.xlabel('Размер матрицы')
plt.ylabel('Время выполнения, мс')
plt.title('Время выполнения в зависимости от размера матрицы')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('images/time_vs_size.jpg', format='jpg', dpi=300)
plt.close()

plt.figure(figsize=(10, 6))
plt.plot(sizes, speedup_2, marker='o', label='S(2)')
plt.plot(sizes, speedup_4, marker='o', label='S(4)')
plt.xlabel('Размер матрицы')
plt.ylabel('Ускорение')
plt.title('Ускорение в зависимости от размера матрицы')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('images/speedup_vs_size.jpg', format='jpg', dpi=300)
plt.close()

print("Plots saved:")
print("images/time_vs_size.jpg")
print("images/speedup_vs_size.jpg")
