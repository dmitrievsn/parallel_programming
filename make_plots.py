import os
import matplotlib.pyplot as plt

sizes = [200, 400, 800, 1200, 1600, 2000]

times_8 = [1.227, 2.737, 19.6923, 65.4767, 154.831, 250.799]
times_16 = [0.6037, 2.8573, 19.4299, 64.8586, 152.335, 242.029]
times_32 = [0.5809, 2.9101, 19.6265, 66.127, 150.328, 248.106]

os.makedirs("images", exist_ok=True)

plt.figure(figsize=(10, 6))
plt.plot(sizes, times_8, marker='o', label='8x8')
plt.plot(sizes, times_16, marker='o', label='16x16')
plt.plot(sizes, times_32, marker='o', label='32x32')
plt.xlabel('Размер матрицы')
plt.ylabel('Время выполнения, мс')
plt.title('Время выполнения CUDA-программы')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('images/time_vs_size.jpg', format='jpg', dpi=300)
plt.close()

best_times = []
best_blocks = []

for i in range(len(sizes)):
    vals = [(times_8[i], 8), (times_16[i], 16), (times_32[i], 32)]
    best = min(vals)
    best_times.append(best[0])
    best_blocks.append(best[1])

plt.figure(figsize=(10, 6))
plt.plot(sizes, best_blocks, marker='o')
plt.xlabel('Размер матрицы')
plt.ylabel('Лучший размер блока')
plt.title('Лучшая конфигурация блоков в зависимости от размера матрицы')
plt.grid(True)
plt.tight_layout()
plt.savefig('images/best_block_vs_size.jpg', format='jpg', dpi=300)
plt.close()

print("Plots saved:")
print("images/time_vs_size.jpg")
print("images/best_block_vs_size.jpg")