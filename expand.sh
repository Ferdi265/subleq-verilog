#!/bin/bash

if [[ $# -gt 2 || $# -eq 0 ]]; then
    usage
fi

file=$1
shift

if [[ ! -f "$file" ]]; then
    echo "error: '$file' doesn't exist" >&2
    usage
fi

lines=$(wc -l "$file" | cut -d\  -f1)
count=${1:-65536}
rest=$(($count - $lines))

for i in $(seq 0 $(($rest - 1))); do
    echo 0000 >> "$file"
done
