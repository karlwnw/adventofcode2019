package main

import (
	"testing"
)

func TestFuel(t *testing.T) {
	got12 := Fuel(12)
	if got12 != 2 {
		t.Errorf("2 = %d; want 2", got12)
	}

    got14 := Fuel(14)
    if got14 != 2 {
        t.Errorf("2 = %d; want 2", got14)
    }
}

func TestTotalFuel(t *testing.T) {
    got14 := TotalFuel(14)
    if got14 != 2 {
        t.Errorf("2 = %d; want 2", got14)
    }

    got1969 := TotalFuel(1969)
    if got1969 != 966 {
        t.Errorf("966 = %d; want 966", got1969)
    }
}