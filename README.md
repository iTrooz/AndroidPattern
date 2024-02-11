# Attempt 1
Naive implementation in Python. Works for size=3 but not for size=5 (way too slow)

time for size=3 -> 8.6s

# Attempt 2

I used [frame graphs](https://brendangregg.com/flamegraphs.html) to determine what was taking so long in the program. Using the screenshot below, I found out that `to_number()` was taking way to much time. After optimising it, the program was faster

Before
![](attempt1.svg)
After (3.6s for size=3)
![](attempt2.svg)

# Attempt 3
According to the flame graph, the next thing that was taking too much time was `__eq__()`, but I wasn't doing class comparison in my code. Searching online, I found out that it was the list contains operator (`in`) that was doing that, because lists aren't hash-based. Following https://stackoverflow.com/a/53657523 I replaced my list with a dict, and the program was faster (2.4s for size=3)

![](attempt3.svg)