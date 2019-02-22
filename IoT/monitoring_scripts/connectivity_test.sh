#! /bin/bash
red='\e[1;31m%s\e[0m'
grn='\e[1;32m%s\e[0m'
end=$'\e[0m'

while :
do
    clear;
    echo "Host {SSH} Test";
    IP=("192.168.1.51"
        "192.168.1.52"
        "192.168.1.53"
        "192.168.1.54"
        "192.168.1.55"
        "192.168.1.56"
        "192.168.1.57"
        "192.168.1.58"
        "192.168.1.59"
        "192.168.1.60"
        "192.168.1.99");
    for i in "${IP[@]}"
    do
        nc -v -z -G 1 $i 22 &> /dev/null && printf "%-15s : $grn %s $end \n" $i "Online" || printf "%-15s : $red %s $end \n" $i "Offline";
    done ;
    sleep 2;
done
