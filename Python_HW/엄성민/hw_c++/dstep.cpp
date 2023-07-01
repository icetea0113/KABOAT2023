#include <iostream>
#include <algorithm>

using namespace std;

void printPlus();
void printBlock();

int main() {

    int h;
    while (1) {
        cout << "���̸� �Է��ϼ���";
        cin >> h;
        if (h > 0 && h<100) {
            break;
        }
        else cout << " 0���� ũ�� 100���� ���� ���� �ٽ� �Է��ϼ���" << endl;
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
    //string을 return 해주는 것이 어땠나.
}
void printBlock() {
    std::cout << "|  ";
}//finish