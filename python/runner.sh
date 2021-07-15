#!/bin/bash
echo "provide analysis file: input output"

for number in {1..9}
do
python main.py -p 1000000 --bound --plk1 --threeD --slice --settings settingsTemplate &
sleep 60
done
wait

#python analyzer.py -f $1 -o $2

exit 0

