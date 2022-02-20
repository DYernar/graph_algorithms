package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type Node struct {
	Val       int
	Neighbors []*Node
}

func main() {
	file, err := os.Open("graph.txt")
	if err != nil {
		fmt.Println(err)
		return
	}

	scanner := bufio.NewScanner(file)

	n := -1
	g := make(map[int]*Node)
	for scanner.Scan() {
		val := scanner.Text()

		if n == 0 {
			n, err = strconv.Atoi(val)
			if err != nil {
				fmt.Println("Converting err ", err)
				return
			}
			continue
		}

		first := val[0] - 48
		second := val[1] - 48

		if _, ok := g[int(first)]; !ok {
			g[int(first)] = &Node{Val: int(first), Neighbors: []*Node{}}
		}

		if _, ok := g[int(second)]; !ok {
			g[int(second)] = &Node{Val: int(second), Neighbors: []*Node{}}
		}

		g[int(first)].Neighbors = append(g[int(first)].Neighbors, g[int(second)])
		g[int(second)].Neighbors = append(g[int(second)].Neighbors, g[int(first)])
	}

	fmt.Println(g)
}
