#include <iostream>
#include <string>
#include <vector>
#define REP(i, n) for (int i = 0; (i) < (int)(n); ++ (i))
#define REP3(i, m, n) for (int i = (m); (i) < (int)(n); ++ (i))
#define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))
#define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))
#define ALL(x) ::std::begin(x), ::std::end(x)
using namespace std;


auto solve(int64_t N, int Q, const std::vector<int64_t> &a, const std::vector<int64_t> &b, const std::vector<int64_t> &c, const std::vector<int64_t> &d) {
    // TODO: edit here
}

// generated by oj-template v4.8.1 (https://github.com/online-judge-tools/template-generator)
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int64_t N;
    int Q;
    std::cin >> N >> Q;
    std::vector<int64_t> a(Q), b(Q), c(Q), d(Q);
    REP (i, Q) {
        std::cin >> a[i] >> b[i] >> c[i] >> d[i];
    }
    auto ans = solve(N, Q, a, b, c, d);
    REP (i, Q) {
        std::cout << e[i] << '\n';
    }
    return 0;
}
