defmodule Day3 do
  @moduledoc """
    iex -S mix
    Day3.part1()

    todo
  """

  def part1(input) do
    input
    |> parse

    # |> IO.inspect(label: "part1")
  end

  def parse(input) do
    input
    |> String.split("\n", trim: true)
    |> Enum.map(&String.to_integer/1)
  end
end
