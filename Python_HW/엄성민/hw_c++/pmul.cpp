#include <iostream>
#include <vector>

using namespace std;

int main() {

    int a1;
    vector<int> num1;
    vector<int> num2;

    cout << "숫자를 다 적고, 다 적고 99 입력"<<endl;
    while (cin >> a1) {
        if (a1 == 99) { break; }
        num1.push_back(a1);
    }
    cout << "알파뱃으로 숫자를 입력하세요, 다 적고 99 입력"<<endl;
    while (cin >> a1) {
        if (a1 == 99) { break; }
        num2.push_back(a1);
    }

    
    int num1_size = num1.size();
    int num2_size = num2.size();
    int max_num = num1[0] + num2[0];
    int* result_arr = new int[max_num+1];
    for (int i = 0; i <= max_num; i++) {
        result_arr[i] = 0;
    }
    int num_val;
    int num_x;
    for (int i = 0; i < num1_size-1; i += 2) {
        for (int j = 0; j < num2_size-1; j += 2) {
            num_x = num1[i] + num2[j];
            num_val = num1[i + 1] * num2[j + 1];
            result_arr[num_x] += num_val;
        }
    }

    for (int i = max_num; i >=0 ; i--) {
        cout << result_arr[i] << " ";
    }

    delete[] result_arr;
    
    return 0;
}// finish