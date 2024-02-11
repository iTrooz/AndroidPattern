# Attempt 1
Naive implementation in Python. Works for size=3 but not for size=5 (way too slow)

# Attempt 2

I used [frame graphs](https://brendangregg.com/flamegraphs.html) to determine what was taking so long in the program. Using the screenshot below, I found out that `to_number()` was taking way to much time. After optimising it, the program was faster

Before
![](attempt1.svg)
After
![](attempt2.svg)