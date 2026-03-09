#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <iomanip>
#include <omp.h>

using namespace std;
using namespace std::chrono;

int main(int argc, char* argv[]) {
    int num_threads = 1;

    if (argc > 1) {
        num_threads = stoi(argv[1]);
    }

    ifstream fa("matrix_a.txt");
    ifstream fb("matrix_b.txt");

    if (!fa) {
        cout << "Error: cannot open matrix_a.txt" << endl;
        return 1;
    }

    if (!fb) {
        cout << "Error: cannot open matrix_b.txt" << endl;
        return 1;
    }

    int n1, n2;
    fa >> n1;
    fb >> n2;

    if (n1 <= 0 || n2 <= 0) {
        cout << "Error: wrong matrix size" << endl;
        return 1;
    }

    if (n1 != n2) {
        cout << "Error: matrix sizes are different" << endl;
        return 1;
    }

    int n = n1;

    vector<vector<double>> a(n, vector<double>(n));
    vector<vector<double>> b(n, vector<double>(n));
    vector<vector<double>> c(n, vector<double>(n, 0.0));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (!(fa >> a[i][j])) {
                cout << "Error: wrong data in matrix_a.txt" << endl;
                return 1;
            }
        }
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (!(fb >> b[i][j])) {
                cout << "Error: wrong data in matrix_b.txt" << endl;
                return 1;
            }
        }
    }

    omp_set_num_threads(num_threads);

    auto start = high_resolution_clock::now();

    #pragma omp parallel for
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }

    auto finish = high_resolution_clock::now();
    double time_ms = duration<double, milli>(finish - start).count();

    ofstream fc("result.txt");
    if (!fc) {
        cout << "Error: cannot create result.txt" << endl;
        return 1;
    }

    fc << n << endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            fc << fixed << setprecision(6) << c[i][j];
            if (j < n - 1) {
                fc << " ";
            }
        }
        fc << endl;
    }

    long long volume = 1LL * n * n * n + 1LL * n * n * (n - 1);

    cout << "Matrix size: " << n << "x" << n << endl;
    cout << "Threads: " << num_threads << endl;
    cout << "Execution time (ms): " << time_ms << endl;
    cout << "Task volume: " << volume << endl;
    cout << "Result file: result.txt" << endl;

    return 0;
}