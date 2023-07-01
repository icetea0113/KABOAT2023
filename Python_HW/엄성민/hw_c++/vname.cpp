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
    cout << "������ �Է��ϼ���"<<endl;
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

    // map을 사용하는게 더 좋지 않았나 생각.
    
    //�빮�� ����, a, the ���ֱ� ��ġ�� ���ֱ�, ���� �տ� �ִ°� ����
    int word_size = words.size();
    //�빮�� �ҹ��ڷ�
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