port=$1
portused=0
for i in $(ls /var/lib/redis/)
do
    if [ "$i" == "$port" ]; then
        portused=1
    fi
done
for i in $(ls /etc/redis/ | grep ".conf")
do
    if [ "${i}" == "$port.config" ]; then
        portused=1
    fi
done
if [ "$portused" == "1" ]; then
    echo "Port is used"
else
    echo "Cloning new redis instance with port: $port"
    cp /etc/redis/6379.conf /etc/redis/$port.conf
    mkdir /var/lib/redis/$port
    sed -i "s/6379/$port/g" /etc/redis/$port.conf
    redis-server /etc/redis/$port.conf
fi
