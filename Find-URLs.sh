#!/bin/bash

usage() {
    echo "Usage: $0: [-o out_file] url"
}

out_file="out.csv"
while getopts "ho:" opt
do
    case $opt in
    o)  out_file="$OPTARG";;
    h)  usage
        echo "Overwrites out_file"
        exit 0;;
    ?)  usage
        exit 1;;
    esac
done

# Input url
shift $(( $OPTIND - 1 ))
if [[ $1 = "" ]]
then
    echo "Error: no url input"
    usage
    exit 1
fi
url="$1"
echo "" > "$out_file"
"./.venv/bin/python3.14" main.py "$url" "$out_file"
echo ""
echo "API URLs"
echo "-------------------------"
cat "$out_file"
echo "-------------------------"
echo ""
