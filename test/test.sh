#!/bin/bash

SCRIPTDIR=$(dirname $(realpath $0))

asmtest() {
    "$SCRIPTDIR"/asm/hldemacro.sh <(sed "s/@@A@@/$2/;s/@@B@@/$3/" "$1") /tmp/out.sbl
    "$SCRIPTDIR"/asm/compile.sh /tmp/out.sbl /tmp/memory.hex raw
}

localtest() {
    echo "  ff00: $(printf '%04x' $1) $(printf '%04x' $2) $(printf '%04x' $(($1+$2)))"
}

verilogtest() {
    pushd "$SCRIPTDIR"/.. >/dev/null
    ./subleq +autotest
    popd >/dev/null
}

randtest() {
    a=$((RANDOM % 65536))
    b=$((RANDOM % 65536))

    asmtest "$1" $a $b
    diff <(localtest $a $b) <(verilogtest)
}

for i in $(seq 0 100); do
    echo -n .
    randtest "$1"
done
echo
