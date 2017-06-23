#!/bin/sh -x 

if(($#<1))
then
	echo "usage: $0 model_name"
	exit -1
fi
model=$1

num1=`grep -n "^$" $model|head -3|tail -1|sed 's/://g'`
num2=`grep -n "^$" $model|head -4|tail -1|sed 's/://g'`
num3=$(( $num2 - 1 ))

head -$num3 $model|sed "1,${num1}d" > $model.temp1
cat $model|sed "1,${num2}d" > $model.temp2

