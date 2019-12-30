defmodule Day1Test do
  use ExUnit.Case
  doctest Day1

  test "fuel for mass=13 is 2" do
    assert Day1.calculate_fuel(13) == 2
  end

  test "test parse" do
    assert Day1.parse("12\n14\n1969\n100756") == [12, 14, 1969, 100_756]
  end

  test "part1 adds all fuel values" do
    assert Day1.part1("12\n14\n1969\n100756") == 2 + 2 + 654 + 33583
  end

  test "calculate_recursive_fuel for 12" do
    assert Day1.calculate_recursive_fuel_impl1(12) == 2
  end

  test "calculate_recursive_fuel for 1969" do
    assert Day1.calculate_recursive_fuel_impl1(1969) == 966
  end

  test "calculate_recursive_fuel for 100756" do
    assert Day1.calculate_recursive_fuel_impl1(100_756) == 50346
  end

  test "part2 for [1969, 100_756]" do
    assert Day1.part2("1969\n100756") == 966 + 50346
  end
end
