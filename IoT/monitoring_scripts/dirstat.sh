#! /bin/bash

grn='\e[1;32m%s\e[0m'
end='\e[0m'

while :
do
    clear;
    Volumes=("/Volumes/0" "/Volumes/1" "/Volumes/2" "/Volumes/3");
    echo "Monitoring /Volumes";
    for vol in "${Volumes[@]}"
    do
        printf "%-10s : $grn %-10s $end \n" $vol $(du -hs $vol | cut -f1);
    done;
    sleep 2;
done
