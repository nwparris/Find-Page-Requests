#!/bin/bash

./.venv/bin/python3.14 main.py $1 $2 $3
echo ""
echo "API URLs"
echo "-------------------------"
cat out.csv
echo "-------------------------"
echo ""
