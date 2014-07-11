#!/usr/bin/python
# coding: utf-8

import collections
import json
import MySQLdb

from secret import db_settings

def usage():
	print "..."

def sql():
	"""
	Goal: 
		year AD Ohjaus ...
		1990 3  1
		1991 4  2
		...
	"""
	db = MySQLdb.connect(host=db_settings.host, user=db_settings.user, passwd=db_settings.passwd, db=db_settings.db, charset='utf8')
	cur = db.cursor()
	cur.execute("""
		SELECT category, year, count(*) c
		FROM tekijat
		WHERE category != ""
		GROUP BY category, year
	""")

	data = {}
	years = set()
	categories = set()
	
	for row in cur.fetchall():
		category, year, count = row
		if year not in data:
			data[year] = collections.defaultdict(int)

		data[year][category] = count
		categories.add(category)
		years.add(year)

	catlist = sorted(list(categories))
	res = [['year'] + catlist]
	for y in sorted(list(years)):
		temp = [y]
		for c in catlist:
			temp.append(int(data[y][c]))
		res.append(temp)

	return res

def main():
	print json.dumps(sql())

if __name__ == '__main__':
	main()
