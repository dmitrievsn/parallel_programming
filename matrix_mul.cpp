#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>
#include <iomanip>

using namespace std;
using namespace std::chrono;

vector<vector<double>> readMatrix(const string& filename, int& n) {
    ifstream fin(filename);
    if (!fin) {
        cout << "Error: cannot open " << filename << endl;
        exit(1);
    }
    fin >> n;
    if (n <= 0) {
        cout << "Error: wrong matrix size in " << filename << endl;
        exit(1);
    }
    vector<vector<double>> a(n, vector<double>(n));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            fin >> a[i][j];
        }
    }
    fin.close();
    return a;
}

void writeMatrix(const string& filename, const vector<vector<double>>& c) {
    ofstream fout(filename);
    int n = c.size();
    fout << n << endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            fout << fixed << setprecision(6) << c[i][j];
            if (j != n - 1) {
                fout << " ";
            }
        }
        fout << endl;
    }
    fout.close();
}

int main() {
    int n1, n2;
    vector<vector<double>> a = readMatrix("matrix_a.txt", n1);
    vector<vector<double>> b = readMatrix("matrix_b.txt", n2);
    if (n1 != n2) {
        cout << "Error: matrix sizes are different" << endl;
        return 1;
    }
    int n = n1;
    vector<vector<double>> c(n, vector<double>(n, 0.0));
    auto start = high_resolution_clock::now();
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    auto finish = high_resolution_clock::now();
    double time_ms = duration<double, milli>(finish - start).count();
    writeMatrix("result.txt", c);
    long long volume = 1LL * n * n * n + 1LL * n * n * (n - 1);
    cout << "Matrix size: " << n << "x" << n << endl;
    cout << "Execution time (ms): " << time_ms << endl;
    cout << "Task volume: " << volume << endl;
    cout << "Result file: result.txt" << endl;
    return 0;
}