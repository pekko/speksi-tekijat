#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )" 
cd $DIR

python update_db.py

for i in ./sql/*.sql; 
 	do ./gen.sh $i; 
done

python ./first-year.py > ~/www/speksi/tekijat/data/first-year.json

cd $OLDPWD
