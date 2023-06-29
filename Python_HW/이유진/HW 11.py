class SlopeCalculationException(Exception):
    pass

try:
    x1, y1 = map(int, input().split())
    x2, y2 = map(int, input().split())

    if x1 == x2:
        raise SlopeCalculationException(f"({abs(y2 - y1):.2f})")

    slope = (y2 - y1) / (x2 - x1)
    print(f"{slope:.2f}")
except SlopeCalculationException as e:
    print(e)
