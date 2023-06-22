#include <iostream>
#include <sstream>
#include <vector>
#include <algorithm>


using namespace std;
bool containsNumber(const string& str) {
    for (char c : str) {
        if (!(isdigit(c) or ' ')) {
            return false;  
        }
    }
    return true;  
}

void count_year(int year,int* list ) {
    int a = year % 12;
    list[a]++;
}

int main() {

    string input;
    
    cout << "숫자들을 공백으로 구분하여 입력하세요: ";
    getline(cin, input);
    while (!containsNumber(input)) {
        getline(cin, input);
        cout << "숫자와 공백만 입력하세요" << endl;
    }

    string animal_list[12] = { "Monkey","Rooster","Dog","Pig","RAt","Ox","Tigger",
        "Rabbit","Dragon","snake","Horse","Sheep" };
    vector<int> numbers; 

    istringstream iss(input); 
    int count[12] = { 0 };
    int num;
    while (iss >> num) { 
        numbers.push_back(num);  
    }
    int total_number = 0;

    for (int num : numbers) {
        count_year(num, count);
        //숫자들 함수에 넣어서 나눠서 확인
    }
    for (int i = 0; i < 12; i++) {
        if (count[i] != 0) {
            total_number++;
        }
    }
    auto maxIt = max_element(numbers.begin(), numbers.end());
    int maxValue = *maxIt;
    int k = maxValue % 12;

    cout << total_number << "  " << animal_list[k];


    return 0;
}//finish