#include <iostream>

#include <string>

using namespace std;


void swapCharacters(string& str, int index1, int index2) {
    char temp = str[index1];
    str[index1] = str[index2];
    str[index2] = temp;
}

bool isVowel(char c) {
    // 모음 집합
    string vowels = "aeiouAEIOU";

    // c가 모음인지 확인
    if (vowels.find(tolower(c)) != string::npos) {
        return true;
    }
    else {
        return false;
    }
}
void scan_a(string& word, string& copy, int word_length, int count) {
    for (int i = 0; i < word_length - 1; i++) {
        swapCharacters(word, i, i + 1);
        if (isVowel(word[i])) {
            //word[i] = '*';

        }
        else if(count == 2 && word[i]=='#') {
                word[i] = copy[i];
        }else{
            word[i] = '*';
        }
     
        cout << word << endl;
    }
}

void scan_b(string& word, string& copy, int word_length, int count) {
    for (int i = word_length - 1; i > 0; i--) {
        swapCharacters(word, i, i - 1);
        if (isVowel(word[i])) {
            word[i] = '#';

        }
        else {
            //word[i] = '$';  
        }
        if (count == 2) {
            if (word[i] == '*') {
                word[i] = copy[i];
            }
        }
        cout << word << endl;
    }
}

bool containsNumber(const string& str) {
    for (char c : str) {
        if (isdigit(c)) {
            return true;
        }
    }
    return false;
}

int main() {

    string word;
    
    int num;
    int count = 1;// count가 2라면? 추가 기능


    cout << "문자를 입력하세요(양옆 중 하나에 |)" << endl;
    while (1) {
        std::cin >> word;
        if (containsNumber(word)) {
            cout << "문자열만 입력하세요" << endl;
        }
        else {
            break;
        }
    }
    int word_length = word.size();
    string word_copy = word;
    // 왼쪽에서 오른쪽
    if (word[0] == '|' && word[word_length]!='|') {
        scan_a(word, word_copy, word_length, count);
        count++;
        scan_b(word, word_copy, word_length, count);
    }
    else if (word[0] != '|' && word[word_length - 1] == '|') {
        scan_b(word, word_copy, word_length, count);
        count++;
        scan_a(word, word_copy, word_length, count);
    }
    else cout << "양끝에 |가 없거나 둘다 있어요 ^____^";



    return 0;
}//finish
