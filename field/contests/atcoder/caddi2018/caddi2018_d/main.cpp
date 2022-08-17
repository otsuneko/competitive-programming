#include <iostream>
#include <string>
#include <vector>
#define REP(i, n) for (int i = 0; (i) < (int)(n); ++ (i))
#define REP3(i, m, n) for (int i = (m); (i) < (int)(n); ++ (i))
#define REP_R(i, n) for (int i = (int)(n) - 1; (i) >= 0; -- (i))
#define REP3R(i, m, n) for (int i = (int)(n) - 1; (i) >= (int)(m); -- (i))
#define ALL(x) ::std::begin(x), ::std::end(x)
using namespace std;

constexpr int64_t MOD = 998244353;
int64_t solve(auto N, auto M, const std::vector<auto> &a, const std::vector<auto> &b, const std::vector<auto> &c) {
    // TODO: edit here
}

// generated by oj-template v4.8.1 (https://github.com/online-judge-tools/template-generator)
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    auto N, M;
    std::cin >> N >> M;
    std::vector<auto> a(M), b(M), c(M);
    REP (i, M) {
        std::cin >> a[i] >> b[i] >> c[i];
    }
    auto ans = solve(N, M, a, b, c);
    std::cout << ans << '\n';
    return 0;
}
