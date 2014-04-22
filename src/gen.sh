#!/bin/bash

source ./secret/db_settings.py

DIR="$( cd "$( dirname "$0" )" && pwd )"
TARGET=$DIR/../graphs/$(basename $1 .sql).htm
mysql --host=$host --user=$user --password=$passwd $db --html < $1 > $TARGET
echo '<pre>' >> $TARGET
cat $1 >> $TARGET
