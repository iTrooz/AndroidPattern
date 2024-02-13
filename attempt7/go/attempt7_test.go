package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIsCloseInt(t *testing.T) {
	assert.True(t, isCloseInt(5.00001))
	assert.True(t, isCloseInt(5.99999))
	assert.True(t, isCloseInt(-5.00001))
	assert.True(t, isCloseInt(-5.99999))
	assert.True(t, !isCloseInt(5.5))
}

func TestGetInbetweenPoints(t *testing.T) {
	assert.Equal(t, getInbetweenPoints([2]int{0, 0}, [2]int{3, 3}), [][2]int{{1, 1}, {2, 2}})
	assert.Equal(t, getInbetweenPoints([2]int{3, 3}, [2]int{0, 0}), [][2]int{{1, 1}, {2, 2}})
	assert.Equal(t, getInbetweenPoints([2]int{1, 1}, [2]int{3, 5}), [][2]int{{2, 3}})
	assert.Equal(t, getInbetweenPoints([2]int{0, 0}, [2]int{0, 2}), [][2]int{{0, 1}})
	assert.Equal(t, getInbetweenPoints([2]int{0, 0}, [2]int{2, 0}), [][2]int{{1, 0}})
}

func TestExclRange(t *testing.T) {
	assert.Equal(t, exclRange(1, 5), []int{2, 3, 4})
	assert.Equal(t, exclRange(5, 1), []int{2, 3, 4})
	assert.Equal(t, exclRange(0, 0), []int{})
}
