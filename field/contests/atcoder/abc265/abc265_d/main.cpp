#include <iostream>
#include <string>
#include <vector>
#define REP(i, n) for (int i = 0; (i) < (int)(n); ++ (i))
#define REP3(i, m, n) for (int i = (m); (i) < (int)(n); ++ (i))
#define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))
#define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))
#define ALL(x) ::std::begin(x), ::std::end(x)
using namespace std;

const std::string YES = "Yes";
const std::string NO = "No";
bool solve(int N, int64_t P, int64_t Q, int64_t R, const std::vector<int64_t> &A) {
    // TODO: edit here
}

// generated by oj-template v4.8.1 (https://github.com/online-judge-tools/template-generator)
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int N;
    int64_t P, Q, R;
    std::cin >> N;
    std::vector<int64_t> A(N);
    std::cin >> P >> Q >> R;
    REP (i, N) {
        std::cin >> A[i];
    }
    auto ans = solve(N, P, Q, R, A);
    std::cout << (ans ? YES : NO) << '\n';
    return 0;
}
