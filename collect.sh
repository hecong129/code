#!/bin/sh
####################################################################################
# Name: collect.sh
# version: 1.0 
# Author: jiangdong@staff.sina.com.cn 
# Description: collect system and mysql performace data 
# Last update: 2013-05-02
# created: 2013-01-10
# modified:
# 2013-05-02 if any parameter is null, exit and rm runfile
# 
#####################################################################################
INTERVAL=5
PREFIX=$INTERVAL-Sec-Status 
RUNFILE=running

dir=$1
mode=$2
port=$3

if [[ $dir = "" ]] || [[ $mode = "" ]];then
	echo "dir is null or port is null or mode is null"
	rm -rf $RUNFILE
	exit 
fi


touch $RUNFILE

if [[ ! -d $dir ]];then
	mkdir $dir
fi

# system data
nohup dstat -Tldrcnm --disk-util --output $dir/dstat.txt >/dev/null & 

# disk data
nohup iostat -xdt /dev/sdb 5 > $dir/iostat.txt &

if [[ $mode = "oltp" ]];then

# response time
./tcprstat -p $port -t 5 -n 0 > $dir/rps.txt &

# mysql data
while test -e $RUNFILE; do
	file=$(date +%F_%I)
	sleep=$(date +%s.%N | awk "{print $INTERVAL - (\$1 % $INTERVAL)}")
	sleep $sleep
	ts="$(date +"TS %s.%N %F %T")"
	loadavg="$(uptime)"
	echo "$ts $loadavg" >> $dir/$PREFIX-${file}-Status
#	mysql -umysqlha -pJxh2MnxeHw -S/tmp/mysql${port}.sock -e 'SHOW GLOBAL STATUS' >> $dir/$PREFIX-${file}-Status &
	echo "$ts $loadavg" >> $dir/$PREFIX-${file}-innodbstatus
#	mysql -umysqlha -pJxh2MnxeHw -S/tmp/mysql${port}.sock -e 'SHOW ENGINE INNODB STATUS\G' >> $dir/$PREFIX-${file}-innodbstatus & echo "$ts $loadavg" >> $dir/$PREFIX-${file}-processlist
#	mysql -umysqlha -pJxh2MnxeHw -S/tmp/mysql${port}.sock -e 'SHOW FULL PROCESSLIST\G' >> $dir/$PREFIX-${file}-processlist &
	#echo $ts
done

else

while test -e $RUNFILE; do
	sleep 1
done

fi

ps -ef|grep tcprstat|grep -v grep|awk '{print $2}'|xargs kill
ps -ef|grep dstat|grep -v grep|awk '{print $2}'|xargs kill
ps -ef|grep iostat|grep -v grep|awk '{print $2}'|xargs kill

echo Exiting because $RUNFILE does not exist.
exit
