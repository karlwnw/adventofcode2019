#!/bin/sh
set -e

# Usage: ./fetchinput 1

DAY=$1
URL="https://adventofcode.com/2019/day/$DAY/input"
SESSIONCOOKIE="`cat .sessioncookie`"
INPUTFILE="inputs/day$DAY.input"

if [ -f $INPUTFILE ]; then
    echo "File $INPUTFILE already exists."
    exit
fi

echo "Downloading input file for day DAY at URL $URL"

curl -s $URL \
  -H "cookie: session=$SESSIONCOOKIE" \
  > $INPUTFILE