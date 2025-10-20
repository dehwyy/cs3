package builder_test

import (
	"patterns/internal/builder"
	"testing"
)

func TestOrderBuilder(t *testing.T) {
	order := builder.New().
		WithItems(
			builder.Item{
				Name:        "Cap",
				Description: "Cap for men",
				Price:       10,
				Currency:    builder.USD,
			},
			builder.Item{
				Name:        "Talon Knife",
				Description: "CS2 | Talon Knife | Boreal Forest",
				Price:       1500,
				Currency:    builder.TRX,
			},
		).
		Build()

	t.Logf("Formed order:\n%s", order)
}
