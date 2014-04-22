#!/usr/bin/python
# coding: utf-8

import csv
import glob
import argparse
import MySQLdb

from secret import db_settings

def usage():
	print "..."

def sql():
	db = MySQLdb.connect(host=db_settings.host, user=db_settings.user, passwd=db_settings.passwd, db=db_settings.db)
	cur = db.cursor()
	cur.execute('SELECT year, first_name, last_name FROM tekijat ORDER BY year')
	
	all_names = set()
	year_names = set()

	lines = []
	this_year = 0
	count_first = 0
	
	for row in cur.fetchall():
		name = row[1]+" "+row[2]
		year = row[0]
		
		if year != this_year:
			if this_year != 0:
				lines.append('[\"%d\", %s, %s]' % (this_year, count_first, len(year_names)))
			this_year = year
			count_first = 0
			year_names = set()
		else:
			year_names.add(name)
			if name not in all_names:
				all_names.add(name)
				count_first += 1

	lines.append('[\"%d\", %s, %s]' % (this_year, count_first, len(year_names)))
	print '['
	print ','.join(lines)
	print ']'

def csv():
	parser = argparse.ArgumentParser(description='to be done')
	
	parser.add_argument('-d', '--debug', action='store_true')

	args = parser.parse_args()

	DATA_DIR = "../data/"
	names = []

	files = [f for f in glob.glob(DATA_DIR+'*.csv')]
	files.sort()
	# last year?
	# files.reverse()

	lines = []

	for filename in files:
		year = filename[-8:-4]
		count_first = 0
		count_all = 0
		names_year = []
		
		etu_index = 0
		suku_index = 0

		if args.debug:
			print
			print year
		with open(filename, 'rb') as f:

			reader = csv.reader(f, delimiter=',', quotechar='"')
			for fields in reader:

				if "Etunimi" in fields:
					etu_index = fields.index("Etunimi")
					suku_index = etu_index -1
					continue

				if len(fields) < etu_index:
					continue

				n = fields[etu_index]+" "+fields[suku_index]
				if n not in names:
					if args.debug:
						print " ",n
					names.append(n)
					count_first += 1
				if n not in names_year:
					names_year.append(n)
					count_all += 1
		lines.append("[\"%s\", %s, %s]" % (year,count_first, count_all))
	print '['
	print ','.join(lines)
	print ']'

def main():
	sql()

if __name__ == '__main__':
	main()
