#!/usr/bin/python
# coding: utf-8

import json
import MySQLdb

from secret import db_settings

def usage():
	print "..."

def do_sql(query):
	db = MySQLdb.connect(host=db_settings.host, user=db_settings.user, passwd=db_settings.passwd, db=db_settings.db, charset='utf8')
	cur = db.cursor()
	cur.execute(query)
	
	res = [row for row in cur.fetchall()]	
	return res

def main():
	import sys
	if len(sys.argv) != 2:
		usage()
		sys.exit(1)

	query = open(sys.argv[1]).read()
	data = do_sql(query)
	print json.dumps(data)

if __name__ == '__main__':
	main()
