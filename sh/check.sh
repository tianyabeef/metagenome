ls  *err*|grep -v "cycle" |while read line;do echo "egrep \"Segment\" $line";done>check.out.sh
ls  *err*|grep -v "cycle" |while read line;do echo "egrep \"Kill\" $line";done>>check.out.sh
ls  *err*|grep -v "cycle" |while read line;do echo "tail -n 2 $line  |head -1 ;echo $line ";done>>check.out.sh
