package builder

import (
	"time"

	"github.com/google/uuid"
)

type OrderBuilder struct {
	items []Item
}

func New() *OrderBuilder {
	return &OrderBuilder{}
}

// `Builder` implementation`
func (o OrderBuilder) Build() *Order {
	return &Order{
		ID:        uuid.New(),
		Items:     o.items,
		CreatedAt: time.Now(),
		Additional: map[string]any{
			"source": "builder",
		},
	}
}

func (o OrderBuilder) WithItems(items ...Item) OrderBuilder {
	o.items = append(o.items, items...)

	return o
}
