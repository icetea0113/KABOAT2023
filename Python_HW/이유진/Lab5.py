def process_string(input_string: str) -> str:
    words = input_string.split()

    if len(words) == 0:
        return "입력된 문자열이 없습니다."

    processed_words = []

    for word in words:
        if word.lower() in ["a", "the"]:
            continue
        if processed_words:
            processed_word = word[0].upper() + word[1:].lower()
        else:
            processed_word = ''.join([ch for ch in word if ch.lower() not in ['a', 'e', 'i', 'o', 'u']])
        processed_words.append(processed_word)

    return ''.join(processed_words)

# 입력 받은 문자열을 처리하여 변환하고 합친 후 한 문장으로 출력
input_string = input("문자열을 입력하세요: ")
processed_sentence = process_string(input_string)
print(processed_sentence)
