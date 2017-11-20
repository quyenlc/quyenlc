hostname=$1
result="$(perl /opt/bin/zabbix/main.pl $hostname)"
if [ "$result" -eq 200 ] || [ "$result" -eq 201 ]
then
    echo 1;
else
    echo 0;
fi
