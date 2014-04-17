#!/usr/bin/python
# *-* encoding: utf-8 *-*

import csv
import glob
import MySQLdb as mdb
import argparse

def usage():
	print "..."

def main():
	con = mdb.connect('db1.kapsi.fi', 'pwc', '--- SALASANA TÄHÄN ---', 'pwc')
	cur = con.cursor()

	parser = argparse.ArgumentParser(description='to be done')
	parser.add_argument('-d', '--debug', action='store_true')

	args = parser.parse_args()

	insert_query = """INSERT INTO tekijat 
		(role, category, subcat1, subcat2, last_name, first_name, year)
	VALUES
		(%s, %s, %s, %s, %s, %s, %s)
	"""

	DATA_DIR = "../data/"
	names = []

	files = [f for f in glob.glob(DATA_DIR+'*.csv')]
	files.sort()

	columns = {
		'Tehtävä' : 0, 
		'Kategoria' : 1, 
		'Alakategoria' : 2,
		'Alakategoria 1' : 2, 
		'Alakategoria 2' : 3, 
		'Sukunimi' : 4, 
		'Etunimi' : 5
	}

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
			
			# first line only
			for header in reader:
				sql_cols = []
				for h in header:
					if h in columns:
						sql_cols.append(columns[h])
					else:
						sql_cols.append(None)
				break
			
			# rest of file
			for row in reader:
				fields = [''] * 6
				for i in xrange(len(sql_cols)):
					if sql_cols[i] is not None:
						fields[sql_cols[i]] = row[i]

				fields.append(year)

				cur.execute(insert_query, tuple(fields))


if __name__ == '__main__':
	main()
