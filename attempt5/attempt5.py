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

def to_number(p):
    return 7-p[1]*3 + p[0]


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

def chooseNextPoint(result: set[int], usedPoints: dict[tuple, None]): # generator of ints
    if len(usedPoints) >= MIN_LEN:
        usedPointsMerged = tuple(c for p in usedPoints for c in p)
        # print(usedPointsMerged)
        result.add(usedPointsMerged)
        # add print(usedPointsStr) here is you want to print all possibilities

        if len(usedPoints) == SIZE*SIZE: # optimisation
            return

    # Calculate all possible next used points and their inbetween points
    for p in itertools.product(range(SIZE), repeat=2):

        if p not in usedPoints: # if true, we can use this point as the next one
            usedPointsCopy = usedPoints.copy()

            # add the point inbetween the last one and the new one. Beware of not adding points already in there
            for between_p in getInbetweenPoints(next(reversed(usedPointsCopy.keys()))  , p):
                if between_p not in usedPointsCopy:
                    usedPointsCopy[between_p] = None

            usedPointsCopy[p] = None
            chooseNextPoint(result, usedPointsCopy)


def main():
    globalResult=set()
    for p in genAllPoints():
        chooseNextPoint(globalResult, {p: None})

        print(f"Finished start point {p}")
    print("Sum:", len(globalResult))

main()
