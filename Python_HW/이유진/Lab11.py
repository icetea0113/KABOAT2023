line = input()
numbers = line.split()
partial_sum = 0
result = ""

try:
    for i, num in enumerate(numbers):
        partial_sum += int(num)
    result = str(partial_sum)
except ValueError:
    result = "(" + str(partial_sum) + ")"

print(result)
