#!/bin/bash

KEY_WORD=$1
EXPECT_PROC_NUMBER=$2

echo "KEY_WORD: $KEY_WORD, EXPECT_PROC_NUMBER: $EXPECT_PROC_NUMBER"
if [ $# == 2 ]
then
    echo 'ps -ef | grep $KEY_WORD | grep -v grep | grep java | wc -l'
    PROC_NUMBER=`ps -ef | grep $KEY_WORD | grep -v grep | grep java | wc -l`
else
    PROC_USER=$3
	PROC_NUMBER=`ps -ef | grep $KEY_WORD | grep -v grep | grep java | awk '{if ($1 == "'${PROC_USER}'") {print $1}}' | wc -l`
fi

if [ "$PROC_NUMBER" == "$EXPECT_PROC_NUMBER" ]; then
    exit 0
else 
    exit -1
fi
