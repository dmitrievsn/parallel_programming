#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <cstdlib>

using namespace std;

__global__ void matMulKernel(double* A, double* B, double* C, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < n && col < n) {
        double sum = 0.0;
        for (int k = 0; k < n; k++) {
            sum += A[row * n + k] * B[k * n + col];
        }
        C[row * n + col] = sum;
    }
}

vector<double> readMatrix(const string& filename, int& n) {
    ifstream fin(filename);
    if (!fin) {
        cout << "Error: cannot open " << filename << endl;
        exit(1);
    }

    fin >> n;
    vector<double> a(n * n);

    for (int i = 0; i < n * n; i++) {
        fin >> a[i];
    }

    return a;
}

void writeMatrix(const string& filename, const vector<double>& c, int n) {
    ofstream fout(filename);
    fout << n << endl;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            fout << c[i * n + j] << " ";
        }
        fout << endl;
    }
}

int main(int argc, char* argv[]) {
    int n;

    vector<double> A = readMatrix("matrix_a.txt", n);
    vector<double> B = readMatrix("matrix_b.txt", n);

    vector<double> C(n * n);

    double *d_A, *d_B, *d_C;

    cudaMalloc(&d_A, n * n * sizeof(double));
    cudaMalloc(&d_B, n * n * sizeof(double));
    cudaMalloc(&d_C, n * n * sizeof(double));

    cudaMemcpy(d_A, A.data(), n * n * sizeof(double), cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, B.data(), n * n * sizeof(double), cudaMemcpyHostToDevice);

    int blockSize = 16;
    if (argc > 1) {
        blockSize = atoi(argv[1]);
    }

    dim3 block(blockSize, blockSize);
    dim3 grid((n + block.x - 1) / block.x,
              (n + block.y - 1) / block.y);

    auto start = chrono::high_resolution_clock::now();

    matMulKernel<<<grid, block>>>(d_A, d_B, d_C, n);
    cudaDeviceSynchronize();

    auto finish = chrono::high_resolution_clock::now();
    double time_ms = chrono::duration<double, milli>(finish - start).count();

    cudaMemcpy(C.data(), d_C, n * n * sizeof(double), cudaMemcpyDeviceToHost);

    writeMatrix("result.txt", C, n);

    cout << "Matrix size: " << n << "x" << n << endl;
    cout << "Block size: " << blockSize << "x" << blockSize << endl;
    cout << "Execution time (ms): " << time_ms << endl;

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);

    return 0;
}