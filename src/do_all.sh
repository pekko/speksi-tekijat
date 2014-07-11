#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )" 
cd $DIR

[ -e ../data ]   || mkdir ../data
[ -e ../graphs ] || mkdir ../graphs

python update_db.py

for i in ./sql/tables/*.sql; 
 	do ./gen.sh $i; 
done

for i in ./sql/json/*.sql;
	do python sql_json.py $i > ../data/$(basename $i .sql).json;
done

python ./first_year.py > ../data/first-year.json

cd $OLDPWD
