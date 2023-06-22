#include <iostream>
#include <iomanip>


using namespace std;

struct Point {
    int x;
    int y;
};

int main() {

    Point p1;
    Point p2;

    std::cout << "첫번째 점의 x,y 값을 스페이스바로 띄어 입력하세요 ";
    std::cin >> p1.x >> p1.y;
    std::cout << "두번째 점의 x,y 값을 스페이스바로 띄어 입력하세요 ";
    std::cin >> p2.x >> p2.y;
    if (p1.x == p2.x) {
        cout << "(" << p1.y - p2.y << ".00)";
    }
    else cout << std::fixed << std::setprecision(2) << double(p2.y - p1.y) / (p2.x - p1.x);

    return 0;
}//finish