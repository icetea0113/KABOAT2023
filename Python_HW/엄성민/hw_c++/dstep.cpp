#include <iostream>
#include <algorithm>

using namespace std;

void printPlus();
void printBlock();

int main() {

    int h;
    while (1) {
        cout << "높이를 입력하세요";
        std::cin >> h;
        if (h > 0 && h<100) {
            break;
        }
        else cout << " 0보다 크고 100보다 작은 수를 다시 입력하세요" << endl;
    }

    for (int flo = 1; flo <= h; flo++) {
        for (int i = 1; i <= flo; i++) {
            printPlus();
        }
        cout << "+" << endl;

        for (int j = 1; j <= flo; j++) {
            printBlock();
        }
        cout << "|" << endl;
    }
    for (int k = 0; k < h; k++) {
        printPlus();
    }
    cout << "+" << endl;

    return 0;

}
void printPlus() {
    std::cout << "+--";
}
void printBlock() {
    std::cout << "|  ";
}//finish