#include<iostream>
#include<algorithm>
#include<cmath>
using namespace std;
int main() {
	int n;
	cin >> n;
	int g = n % 10;
	if (g == 2 || g == 4 || g == 5 || g == 7 || g == 9) {
		cout << "hon";
		return 0;
	}
	else if (g == 0 || g == 1 || g == 6 || g == 8) {
		cout << "pon";
		return 0;
	}
	else {
		cout << "bon";
	}
}
