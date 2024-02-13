package main

import (
	"fmt"
	"math"
)

const SIZE = 4
const MIN_LEN = 4
const MAX_LEN = 7

func isCloseInt(n float64) bool {
	n = math.Mod(math.Abs(n), 1.0)
	eps := 0.0001
	return n < eps || (1.0-n) < eps
}

func toNumber0(p [2]int) int {
	return 6 - p[1]*3 + p[0]
}

func exclRange(a, b int) []int {
	if a > b {
		a, b = b, a
	}
	l := []int{}
	for i := a + 1; i < b; i++ {
		l = append(l, i)
	}
	return l
}

func getInbetweenPoints(p1, p2 [2]int) [][2]int {
	xdiff := p2[0] - p1[0]

	if xdiff == 0 {
		var result [][2]int
		for _, y := range exclRange(p1[1], p2[1]) {
			result = append(result, [2]int{p1[0], y})
		}
		return result
	}

	slope := float64(p2[1]-p1[1]) / float64(xdiff)
	init := float64(p2[1]) - slope*float64(p2[0])

	var result [][2]int
	for _, x := range exclRange(p1[0], p2[0]) {
		y := slope*float64(x) + init
		if isCloseInt(y) {
			result = append(result, [2]int{x, int(math.Round(y))})
		}
	}

	return result
}

func genAllPoints() [][2]int {
	var result [][2]int
	for x := 0; x < SIZE; x++ {
		for y := 0; y < SIZE; y++ {
			result = append(result, [2]int{x, y})
		}
	}
	return result
}

func chooseNextPoint(usedPoints *[][2]int, lastPoint [2]int) int {
	var foundPossibilities int

	if len(*usedPoints) >= MIN_LEN {
		foundPossibilities++
		if len(*usedPoints) == MAX_LEN {
			return foundPossibilities
		}
	}

	for _, p := range genAllPoints() {
		if !containsPoint(*usedPoints, p) {

			valid := true
			for _, betweenP := range getInbetweenPoints(lastPoint, p) {
				if !containsPoint(*usedPoints, betweenP) {
					valid = false
					break
				}
			}

			if valid {
				usedPointsCopy := append(*usedPoints, p)
				foundPossibilities += chooseNextPoint(&usedPointsCopy, p)
			}
		}
	}

	return foundPossibilities
}

func main() {
	var total int

	for _, p := range genAllPoints() {
		fmt.Printf("Starting start point %v (id=%v)\n", p, toNumber0(p))
		usedPoints := [][2]int{p}
		out := chooseNextPoint(&usedPoints, p)
		total += out
		fmt.Printf("Finished start point %v (possibilities=%v)\n", p, out)
	}

	fmt.Printf("Sum: %d\n", total)
}

func containsPoint(points [][2]int, point [2]int) bool {
	for _, p := range points {
		if p == point {
			return true
		}
	}
	return false
}
