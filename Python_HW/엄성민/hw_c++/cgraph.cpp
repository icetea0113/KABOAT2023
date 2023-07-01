#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

using namespace std;

string graph_c(char h, int size_x, int size) {
    string str;
    int air = size_x - size;
    for (int i = 0; i < air; i++) {
        str += " ";
    }
    for (int j = 0; j < size; j++) {
        str += h;
    }


    return str;
}


int main() {

    char h;
    int num;
    vector<int> numbers;

    while (1) {
        cout << "#�� $�� �ϳ��� �����ϼ���"<<endl;
        std::cin >> h;
        if (h == '#' || h == '$') {
            break;
        }
    }


        cout << "77������ ���ڵ��� �Է��ϼ���. �Է��� 77�� �Է��ϼ���"<<endl;
        while (std::cin >> num) {
            if (num >= 77) { break; }
            numbers.push_back(num);
        }
        int size_x = numbers.size();
        int size_y = accumulate(numbers.begin(), numbers.end(), 0);
        string* frame = new string[size_y];
        vector<int> numss;
        int temp_su = numbers.size();
        
        for (int i = 0; i < numbers.size(); i++) {
            while (numbers[i] > 0) {
                numss.push_back(temp_su);
                numbers[i]--;
            }
            temp_su--;
        }

        for (int i = 0; i < size_y; i++) {
            frame[i] = graph_c(h, size_x, numss[i]);
        }
        
        for (int i = 0; i < size_y; i++) {
            if (h == '#') {
                cout << frame[i] << endl;
            }
            else {
                cout << frame[size_y - 1 - i] << endl;
            }
        }


        delete[] frame;
    return 0;
}//finish
