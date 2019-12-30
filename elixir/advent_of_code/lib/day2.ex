defmodule Day2 do
  @moduledoc """
    iex -S mix
    file = File.read!("../../inputs/day2.input")
    Day2.part1(file)
  """

  def part1(input) do
    input
    |> parse
    |> initial_setup
    |> IO.inspect(label: "Part1 original list", limit: :infinity)
    |> compute
  end

  def part2(input) do
    program =
      input
      |> parse
      |> IO.inspect(label: "Part2 original list", limit: :infinity)

    Enum.each(0..99, fn noun ->
      Enum.each(0..99, fn verb ->
        output =
          initial_setup(
            program,
            noun,
            verb
          )
          |> compute

        case output do
          [11_590_668 | _] ->
            IO.puts("Found Part1 value for noun=#{noun} verb=#{verb}")

          [19_690_720 | _] ->
            IO.puts("Found noun=#{noun} verb=#{verb}")
            IO.puts("Answer = #{100 * noun + verb}")
            IO.inspect(output, label: "Part2 output", limit: :infinity)

          _ ->
            IO.puts("Next noun=#{noun} verb=#{verb}")
        end
      end)
    end)
  end

  def initial_setup(program, noun \\ 12, verb \\ 2) do
    {front, [_ | tail]} = Enum.split(program, 1)
    program = front ++ [noun | tail]

    {front, [_ | tail]} = Enum.split(program, 2)
    front ++ [verb | tail]
  end

  def compute(position \\ 0, program) do
    digit = Enum.at(program, position)

    case digit do
      99 ->
        program

      1 ->
        num1_pos = Enum.at(program, position + 1)
        num2_pos = Enum.at(program, position + 2)
        res_pos = Enum.at(program, position + 3)

        result = Enum.at(program, num1_pos) + Enum.at(program, num2_pos)

        {front, [_ | tail]} = Enum.split(program, res_pos)
        program = front ++ [result | tail]
        position = position + 4
        compute(position, program)

      2 ->
        num1_pos = Enum.at(program, position + 1)
        num2_pos = Enum.at(program, position + 2)
        res_pos = Enum.at(program, position + 3)

        result = Enum.at(program, num1_pos) * Enum.at(program, num2_pos)

        {front, [_ | tail]} = Enum.split(program, res_pos)
        program = front ++ [result | tail]
        position = position + 4
        compute(position, program)

      _ ->
        :error
    end
  end

  def parse(input) do
    input
    |> String.trim()
    |> String.split(",", trim: true)
    |> Enum.map(&String.to_integer/1)
  end
end
