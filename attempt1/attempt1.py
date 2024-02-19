from dataclasses import dataclass

SIZE=3
MIN_LEN=4
MAX_SIZE=SIZE*SIZE
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

@dataclass
class Point:
    x: int
    y: int

    def to_number(self):
        match self:
            case Point(0, 0): return 7
            case Point(1, 0): return 8
            case Point(2, 0): return 9

            case Point(0, 1): return 4
            case Point(1, 1): return 5
            case Point(2, 1): return 6

            case Point(0, 2): return 1
            case Point(1, 2): return 2
            case Point(2, 2): return 3

def getInbetweenPoints(p1: Point, p2: Point):
    xdiff = (p2.x-p1.x)
    if xdiff == 0:
        for y in range(min(p1.y, p2.y)+1, max(p1.y, p2.y)):
            yield Point(p1.x, y)
        return
    else:
        slope = (p2.y-p1.y) / (p2.x-p1.x)

    init = p2.y - p2.x*slope

    for x in range(min(p1.x, p2.x)+1, max(p1.x, p2.x)):
        y = slope*x + init
        if is_close_int(y):
            yield Point(x, round(y))


assert list(getInbetweenPoints(Point(0, 0), Point(3, 3))) == [Point(1, 1), Point(2, 2)]
assert list(getInbetweenPoints(Point(3, 3), Point(0, 0))) == [Point(1, 1), Point(2, 2)]
assert list(getInbetweenPoints(Point(1, 1), Point(3, 5))) == [Point(2, 3)]
assert list(getInbetweenPoints(Point(0, 0), Point(0, 2))) == [Point(0, 1)]
assert list(getInbetweenPoints(Point(0, 0), Point(2, 0))) == [Point(1, 0)]

def genAllPoints():
    for x in range(SIZE):
        for y in range(SIZE):
            yield Point(x, y)

def chooseNextPoint(result: set[int], usedPoints: list[Point]): # generator of ints
    if len(usedPoints) >= MIN_LEN:
        usedPointsStr = "".join(str(p.to_number()) for p in usedPoints)
        result.add(usedPointsStr)
        # add print(usedPointsStr) here is you want to print all possibilities

        if len(usedPoints) == MAX_SIZE:
            return

    # Calculate all possible next used points and their inbetween points
    for p in genAllPoints():
            
        if p not in usedPoints: # if true, we can use this point as the next one
            usedPointsCopy = usedPoints.copy()

            # add the point inbetween the last one and the new one. Beware of not adding points already in there
            for between_p in getInbetweenPoints(usedPointsCopy[-1], p):
                if between_p not in usedPointsCopy:
                    usedPointsCopy.append(between_p)

            usedPointsCopy.append(p)
            chooseNextPoint(result, usedPointsCopy)


def main():
    globalResult=set()
    for p in genAllPoints():
        chooseNextPoint(globalResult, [p])

        print(f"Finished start point {p}")
    print("Sum:", len(globalResult))

main()
