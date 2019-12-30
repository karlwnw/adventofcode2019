#!/usr/bin/env ruby

input = ARGF.read
modules = input.split("\n").map(&:to_i)

# Part I
fuel = 0
modules.each do |mass|
  fuel += mass / 3 - 2
end
puts fuel

# or
puts modules.map {|m| m / 3 - 2}.inject(0, :+)

# Part II
fuel = 0


def total_fuel(x)
  x = x / 3 - 2
  x > 0 ? total_fuel(x) + x : 0
end

modules.each do |mass|
  fuel += total_fuel(mass)
end

puts fuel

# or
puts modules.map {|m| total_fuel(m)}.inject(0, :+)
