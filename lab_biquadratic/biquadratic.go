package main

import (
	"context"
	"errors"
	"fmt"
	"math"
	"os"
	"strconv"
)

func getCoefficient(ctx context.Context, name string, args []string, index int) float64 {
	for {
		if len(args) > index {
			value, err := strconv.ParseFloat(args[index], 64)
			if err == nil {
				fmt.Printf("Коэффициент %s=%f\n", name, value)
				return value
			}

			err2 := errors.New("error123")

			errors.Is(err, err2)

			fmt.Println("Некорректное значение для", name)
		}
		fmt.Printf("Введите коэффициент %s: ", name)

		var value float64
		if _, err := fmt.Scan(&value); err == nil {
			return value
		}

		fmt.Println("Некорректное значение, попробуйте снова.")
	}
}

func solveBiquadratic(a, b, c float64) []float64 {
	// Discriminant
	d := b*b - 4*a*c
	fmt.Printf("Дискриминант = %f\n", d)

	// Validate discriminant
	if d < 0 {
		fmt.Println("Действительных корней нет.")
		return []float64{}
	}

	// Use formula
	sqrtD := math.Sqrt(d)
	x1 := (-b + sqrtD) / (2 * a)
	x2 := (-b - sqrtD) / (2 * a)

	// Get roots result as
	roots := []float64{x1}
	if x1 != x2 {
		roots = []float64{x1, x2}
	}

	return roots
}

func main() {
	// Get coefficients
	args := os.Args
	a := getCoefficient("A", args, 1)

	// Validate A
	if a == 0 {
		fmt.Println("Коэффициент A в квадратном уравнении не может быть равен 0.")
		return
	}

	// No rules for B & C
	b := getCoefficient("B", args, 2)
	c := getCoefficient("C", args, 3)

	// Solve
	roots := solveBiquadratic(a, b, c)

	// If ANY roots
	if len(roots) > 0 {
		fmt.Println("Действительные корни:", roots)
		return
	}

	fmt.Println("Корней нет.")
}
