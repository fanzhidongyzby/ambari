#!/bin/bash

KEY_WORD=$1
EXPECT_PROC_NUMBER=$2

echo "KEY_WORD: $KEY_WORD, EXPECT_PROC_NUMBER: $EXPECT_PROC_NUMBER"


PROC_NUMBER=`ps -ef | grep $KEY_WORD | grep -v grep | grep -v thive_check_status|wc -l`

echo "proc_number=$PROC_NUMBER"

if [ "$PROC_NUMBER" == "$EXPECT_PROC_NUMBER" ]; then
    exit 0
else 
    exit -1
fi
