defmodule Day2Test do
  use ExUnit.Case
  doctest Day2

  test "program state test example 1" do
    initial = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    output = [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    assert Day2.compute(0, initial) == output
  end

  test "program state test example 2" do
    initial = [1, 0, 0, 0, 99]
    output = [2, 0, 0, 0, 99]
    assert Day2.compute(initial) == output
  end

  test "program state test example 3" do
    initial = [2, 3, 0, 3, 99]
    output = [2, 3, 0, 6, 99]
    assert Day2.compute(initial) == output
  end

  test "program state test example 4" do
    initial = [2, 4, 4, 5, 99, 0]
    output = [2, 4, 4, 5, 99, 9801]
    assert Day2.compute(initial) == output
  end

  test "program state test example 5" do
    initial = [1, 1, 1, 4, 99, 5, 6, 0, 99]
    output = [30, 1, 1, 4, 2, 5, 6, 0, 99]
    assert Day2.compute(initial) == output
  end
end
