# 첫 번째 다항식 입력 받기
poly1_terms = input().split()
poly1_degrees = []
poly1_coefficients = []

for i in range(0, len(poly1_terms), 2):
    degree = int(poly1_terms[i])
    coefficient = int(poly1_terms[i + 1])
    poly1_degrees.append(degree)
    poly1_coefficients.append(coefficient)

# 두 번째 다항식 입력 받기
poly2_terms = input().split()
poly2_degrees = []
poly2_coefficients = []

for i in range(0, len(poly2_terms), 2):
    degree = int(poly2_terms[i])
    coefficient = int(poly2_terms[i + 1])
    poly2_degrees.append(degree)
    poly2_coefficients.append(coefficient)
# 윗 부분을 함수로 만드는게 어떤가.

result_de = []
ye_deg = poly1_degrees[0] + poly2_degrees[0]
result = {}
for i in range(ye_deg+1):
    result[i] = 0

for i in range(len(poly1_degrees)):
    for j in range(len(poly2_degrees)):
        deg = poly1_degrees[i] + poly2_degrees[j] 
        cof = poly1_coefficients[i] * poly2_coefficients[j]

        if deg not in result_de:
            result[deg] = cof
            result_de.append(deg)
        else:
            result[deg] = result[deg] + cof

# key 값을 기준을 정렬된 딕셔너리 생성 
dic = dict(sorted(result.items(), reverse=True))
Dic = list(dic.values())

for n in Dic:
    print(n, end=' ')