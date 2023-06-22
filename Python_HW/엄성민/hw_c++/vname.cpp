#include <iostream>
#include <vector>
#include <sstream>
#include <string>

using namespace std;

string toLowerCase(const string& str) {
    string result = str;

    for (char& c : result) {
        if (isupper(c)) {
            c = tolower(c);
        }
    }

    return result;
}

bool containCase(const string& str) {
    string word = str;
    string word_list[8] = {"a","the","in", "at","on","to","of","by"};
    for (int i = 0; i < 8; i++) {
        if (str == word_list[i]) {
            return true;
        }
    }

    return false;
}

int main() {

    string input;


    bool b_trivi = false;
    cout << "문장을 입력하세요"<<endl;
    getline(cin,input);
    vector<string> words;
    //cout << input<<endl;
    istringstream iss(input);
    string word;

    while (iss >> word) {
        words.push_back(word);
    }

    string word_list2[5] = { "bool","int","float","complex","list" };
    string word_list3[5] = { "b","i","fp","cplx","ls" };
    //대문자 접근, a, the 없애기 전치사 없애기, 제일 앞에 있는거 수정
    int word_size = words.size();
    //대문자 소문자로
    for (int i = 0; i < word_size; i++) {
        words[i] = toLowerCase(words[i]);
        if (containCase(words[i])) {
            words.erase(words.begin() + i);
            i--;
            word_size = words.size();
        }
        if (i == 0) {
            for (int j = 0; j < 5; j++) {
                if (words[i] == word_list2[j]) {
                    words[i] = word_list3[j];
                }
            }
        }
        //cout << words[i]<<endl;
        if (i != 0 && b_trivi ==false && words[i].size()>3) {
            words[i] = words[i].substr(0, 3);
            b_trivi = true;
        }
    }
    cout << words[0];
    for (int i = 1; i < word_size; i++) {
        cout << "_" << words[i];
    }
    return 0;
}//finish