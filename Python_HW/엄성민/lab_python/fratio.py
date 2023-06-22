if __name__ == "__main__":
    diction_word = {}
    
    sentence_word = input()
    sentence_word = sentence_word.lower()

    for c in sentence_word:
        if c ==' ' or c.isdigit():
            continue
        
        if c in diction_word:
            diction_word[c] += 1
        else:
            diction_word[c] = 1
    sum_word = 0
    max_word = 1
    
    for value in diction_word.values():
        sum_word+=value
        max_word = value if max_word < value else max_word

    print(f"{float(max_word)/sum_word:5.2f}")