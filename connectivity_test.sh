#! /bin/bash
red='\e[1;31m%s\e[0m'
grn='\e[1;32m%s\e[0m'
end=$'\e[0m'

while :
do
    clear;
    echo "Host {SSH} Test";
    IP=("192.168.1.78"
        "192.168.1.79"
        "192.168.1.80"
        "192.168.1.81");
    for i in "${IP[@]}"
    do
        nc -v -z -G 1 $i 22 &> /dev/null && printf "%-15s : $grn %s $end \n" $i "Online" || printf "%-15s : $red %s $end \n" $i "Offline";
    done ;
    sleep 2;
done
