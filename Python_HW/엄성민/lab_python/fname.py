volv = "aeiouAEIOU"
finish_sentence =""

def volv_del(a:str):
    global finish_sentence
    d = ""    
    for c in a:
        if c not in volv:
            d +=c
    finish_sentence += d.lower()
            
def sentenp(a:str):
    global finish_sentence
    d = ""
    if(a != "a" and a != "the"):
        for i in range(len(a)):
            if(i==0):
                d += a[i].upper()
            else:
                d+= a[i].lower()
    finish_sentence += d

if __name__ == "__main__":
    input_sentence = input()
    input_list = input_sentence.split()

    for index, senten in enumerate(input_list):
        if(index ==0):
            volv_del(senten)
        else:
            sentenp(senten)
    print(finish_sentence)
