def find_earliest_zodiac(years):
    zodiac_order = {
        "Rat": 0,
        "Ox": 1,
        "Tiger": 2,
        "Rabbit": 3,
        "Dragon": 4,
        "Snake": 5,
        "Horse": 6,
        "Sheep": 7,
        "Monkey": 8,
        "Rooster": 9,
        "Dog": 10,
        "Pig": 11
    }

    zodiac_counts = {}
    earliest_zodiac = "Pig"

    for year in years:
        zodiac = (year - 4) % 12
        zodiac_name = list(zodiac_order.keys())[list(zodiac_order.values()).index(zodiac)]

        if zodiac_name not in zodiac_counts:
            zodiac_counts[zodiac_name] = 1
        else:
            zodiac_counts[zodiac_name] += 1

        if zodiac_order[zodiac_name] < zodiac_order[earliest_zodiac]:
            earliest_zodiac = zodiac_name

    num_different_zodiacs = len(zodiac_counts)

    return num_different_zodiacs, earliest_zodiac

# 입력 받기
input_years = input().split()
lunar_years = [int(year) for year in input_years]

# 결과 출력
num_zodiacs, earliest_zodiac = find_earliest_zodiac(lunar_years)
print(num_zodiacs, earliest_zodiac)
