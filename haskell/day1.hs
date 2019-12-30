import Data.List

main :: IO ()
main = do
  content <- readFile "./inputs/day1.input"
  let input = map read (lines content)
  let part1 = sum (map fuel input)
  let part2 = sum (map totalFuel input)
  print part1
  print part2

fuel :: Int -> Int
fuel mass = mass `div` 3 - 2

totalFuel :: Int -> Int
totalFuel = sum
          . tail
          . takeWhile (> 0)
          . iterate fuel