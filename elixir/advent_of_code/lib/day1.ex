defmodule Day1 do
  @moduledoc """
    iex -S mix
    file = File.read!("../../inputs/day1.input")
    Day1.part1(file)
  """

  def part1(input) do
    input
    |> parse
    |> Enum.map(&calculate_fuel/1)
    |> Enum.sum()

    # |> IO.inspect(label: "Sum")
  end

  def part2(input) do
    input
    |> parse
    |> Enum.map(&calculate_recursive_fuel_impl1/1)
    |> Enum.sum()
  end

  def parse(input) do
    input
    |> String.split("\n", trim: true)
    |> Enum.map(&String.to_integer/1)
  end

  @doc """
  Calculate required fuel

      iex> Day1.calculate_fuel(12)
      2

      iex> Day1.calculate_fuel(14)
      2

      iex> Day1.calculate_fuel(1969)
      654

      iex> Day1.calculate_fuel(100756)
      33583
  """
  def calculate_fuel(mass) do
    max(div(mass, 3) - 2, 0)
  end

  def calculate_recursive_fuel_impl1(mass) do
    fuel = calculate_fuel(mass)

    if fuel > 0 do
      fuel + calculate_recursive_fuel_impl1(fuel)
    else
      0
    end
  end

  def calculate_recursive_fuel_impl2(mass) do
    calculate_fuel(mass)
    |> Stream.iterate(&calculate_fuel/1)
    |> Stream.take_while(&(&1 > 0))
    |> Enum.sum()
  end

  def calculate_recursive_fuel_impl3(mass) do
    case calculate_fuel(mass) do
      fuel when fuel > 0 -> fuel + calculate_recursive_fuel_impl3(fuel)
      _ -> 0
    end
  end
end
