package builder

import (
	"fmt"
	"time"

	"github.com/google/uuid"
)

type Currency string

const (
	// Fiat currencies
	EUR Currency = "EUR"
	USD Currency = "USD"
	RUB Currency = "RUB"
	// Crypto-currencies
	TRX Currency = "TRX"
	BTC Currency = "BTC"
	ETH Currency = "ETH"
)

type Order struct {
	ID uuid.UUID

	Items []Item

	Additional map[string]any

	CreatedAt    time.Time
	DeliveriedAt *time.Time
}

func (o Order) String() string {
	var items string
	for _, item := range o.Items {
		items += fmt.Sprintf("-%s", item)
	}

	return fmt.Sprintf(
		"ID: %s\nItems: [\n%s]\nAdditional: %v\nCreatedAt: %v\nDeliveriedAt: %v\n",
		o.ID,
		items,
		o.Additional,
		o.CreatedAt,
		o.DeliveriedAt,
	)
}

type Item struct {
	Name        string
	Description string
	Price       float64
	Currency    Currency
}

func (i Item) String() string {
	return fmt.Sprintf(" Name: %s\n  Description: %s\n  Price: %0.2f\n  Currency: %s\n", i.Name, i.Description, i.Price, i.Currency)
}
