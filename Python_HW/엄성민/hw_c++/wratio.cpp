#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

using namespace std;
bool containsNumber(const string& str) {
    for (char c : str) {
        if (isdigit(c)) {
            return true;  
        }
    }
    return false;  
}

double isWhat(char c) {
    // 모음 집합
    string vowels = "aeiouAEIOU";
    string semivowels = "wyWY";
    double num;
    // c가 모음인지 확인
    if (vowels.find(tolower(c)) != string::npos) {
        num = 2.0;
    }
    else if (semivowels.find(tolower(c)) != string::npos) {
        num = 1.5;
    }
    else if (c != ' ') { 
        num = 1.0; 
    }
    else num = 0.0;

    return num;
}

int main() {

    string word;
    cout << "문자열만 입력하세요" << endl;

    while (1) {
        getline(cin, word);
        if (containsNumber(word)) {
            cout << "문자열만 입력하세요" << endl;
        }
        else {
            break;
        }
    }
    

    vector<char> words;
    vector<int> num;
    
    words.push_back(word[0]);
    num.push_back(1);
    
    for (char& c : word) {
        c = std::tolower(c);
    }

    for (int i = 1; i < word.size(); i++) {
        if (word[i] == ' ' or word[i] == '.' or word[i]== ',' or word[i]== '?' or word[i] =='!') {
            word.erase(i, 1);
            i--;
        }
        else {
            for (int j = 0; j <= words.size(); j++) {
                if (j == words.size()) {
                    words.push_back(word[i]);
                    num.push_back(1);
                    break;
                }
                if (word[i] == words[j]) {
                    num[j]++;
                    break;
                }
            }
        }
    }
    double total_val = 0.0;
    int max_num = num[0];
    for (int i = 0; i < words.size(); i++) {
        total_val += isWhat(words[i]) * num[i];
        max_num = max_num > num[i] ? max_num : num[i];
    }
    double max_val = 0.0;
    
    for (int i = 0; i < words.size(); i++) {
        if (num[i] == max_num) {
            if (isWhat(words[i]) * max_num > max_val)
                max_val = isWhat(words[i]) * max_num;
        }

    }
    cout << "분모 : " << total_val << endl;
    cout << "분자 : " << max_val << endl;
    cout << fixed << std::setprecision(3) << max_val / total_val << endl;



    return 0;
}//finish