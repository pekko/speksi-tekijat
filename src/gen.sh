TARGET=../graphs/$(basename $1 .sql).htm
mysql --host=db1.kapsi.fi --user=pwc --password=$(cat ~/.mysqlpass) pwc --html < $1 > $TARGET
echo '<pre>' >> $TARGET
cat $1 >> $TARGET