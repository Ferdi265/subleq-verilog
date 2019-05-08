#!/bin/bash

color() {
    printf '\e['$1';'$2'm'
}

for f in *.py; do
    [[ $f == "test_toy.py" ]] && continue

    echo ">> ${f/.py/}: "
    python $f
    if [[ $? -eq 0 ]]; then
        color 1 32
        echo ">> PASS"
        color 0 0
    else
        color 1 31
        echo ">> FAIL"
        color 0 0
    fi
    echo "-------"
done
