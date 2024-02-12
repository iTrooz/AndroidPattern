import itertools

SIZE=3
MIN_LEN=4
# 389112

def is_close_int(n):
    """Check f a float is close to an int"""
    n = abs(n%1)
    eps = 0.0001
    return n < eps or 1-n < eps

assert is_close_int(5.00001)
assert is_close_int(5.99999)
assert is_close_int(-5.00001)
assert is_close_int(-5.99999)
assert not is_close_int(5.5)

def to_number_1(p):
    return 7-p[1]*3 + p[0]
def to_number_0(p):
    return 6-p[1]*3 + p[0]


def getInbetweenPoints(p1: tuple, p2: tuple):
    xdiff = (p2[0]-p1[0])
    if xdiff == 0:
        for y in range(min(p1[1], p2[1])+1, max(p1[1], p2[1])):
            yield (p1[0], y)
        return
    else:
        slope = (p2[1]-p1[1]) / (p2[0]-p1[0])

    init = p2[1] - p2[0]*slope

    for x in range(min(p1[0], p2[0])+1, max(p1[0], p2[0])):
        y = slope*x + init
        if is_close_int(y):
            yield (x, round(y))


assert list(getInbetweenPoints((0, 0), (3, 3))) == [(1, 1), (2, 2)]
assert list(getInbetweenPoints((3, 3), (0, 0))) == [(1, 1), (2, 2)]
assert list(getInbetweenPoints((1, 1), (3, 5))) == [(2, 3)]
assert list(getInbetweenPoints((0, 0), (0, 2))) == [(0, 1)]
assert list(getInbetweenPoints((0, 0), (2, 0))) == [(1, 0)]

def genAllPoints():
    for x in range(SIZE):
        for y in range(SIZE):
            yield (x, y)

def chooseNextPoint(usedPoints: list[bool], lastPoint: tuple): # generator of ints
    if sum(usedPoints) >= MIN_LEN:
        yield 1

        if sum(usedPoints) == SIZE*SIZE: # optimisation
            return

    # Calculate all possible next used points and their inbetween points
    for p in itertools.product(range(SIZE), repeat=2):
        if not usedPoints[to_number_0(p)]: # if true, we can maybe use this point as a next one

            # do not continue with this point if we would it another while tracing the line
            valid = True
            for between_p in getInbetweenPoints(lastPoint, p):
                if usedPoints[to_number_0(between_p)] == False:
                    valid = False
                    break

            if valid:
                usedPointsCopy = usedPoints.copy()
                usedPointsCopy[to_number_0(p)] = True
                yield sum(chooseNextPoint(usedPointsCopy, p))


def main():
    total=0
    for p in genAllPoints():
        print(f"Starting start point {p} ({to_number_0(p)})")
        usedPoints = [False for _ in range(SIZE*SIZE)]
        usedPoints[to_number_0(p)] = True
        total += sum(chooseNextPoint(usedPoints, p))

        print(f"Finished start point {p}")
    print("Sum:", total)

main()
