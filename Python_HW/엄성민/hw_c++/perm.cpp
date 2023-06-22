#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <string>
#include <cmath>
#include <sstream>

using namespace std;

vector<int> result2;
void pem(vector<int>& original, vector<int> result) {
    int size = original.size();
    
    if (size > 1) {
        for (int i = 0; i < size; i++) {
            vector<int> newVector = original;
            result.push_back(newVector[i]);
            newVector.erase(newVector.begin() + i);
            pem(newVector,result);
            result.pop_back();
        }
        
    }
    else if (size == 1) {
        result.push_back(original[0]);
        int val=0;
        for (int i = result.size() - 1; i >= 0; i--) {
            val += result[i] * pow(10, i);
        }
        auto it = find(result2.begin(), result2.end(), val);
        if (it == result2.end()) {
            result2.push_back(val);
        }
    }
}

int main() {

    string input;
    int count;
    vector<string> num1;
    vector<int> num2;
    cout << "숫자를 영어로 입력하세요" << endl;
    getline(cin, input);
    istringstream iss(input);
    string word;

    while (iss >> word) {
        num1.push_back(word);
    }

    cout << "숫자를 입력하세요"<<endl;
    cin >> count;
    string num_name[10] = {"zero", "one", "two", "three","four","five","six","seven","eight","nine" };
    int num[10] = {0,1,2,3,4,5,6,7,8,9 };
    
    for (int i = 0; i < num1.size(); i++) {
        for (int j = 0; j < 10; j++) {
            if (num1[i] == num_name[j]) {
                num2.push_back(num[j]);
            }
        }
    }
    vector<int> result;

    pem(num2, result);
    sort(result2.begin(), result2.end());
    count--;
    int final = result2[count];
    for (int i = num1.size() - 1; i >= 0; i--) {
        int pow_val = final / pow(10, i);
        for (int j = 0; j < 10; j++) {
            if (pow_val == num[j]) {
                cout << num_name[j] << " ";
            }
        }
        final -= pow_val * pow(10, i);
    }

    return 0;
}