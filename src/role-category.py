import MySQLdb as mdb
from secret import db_settings

con = mdb.connect(db_settings.host, db_settings.user, db_settings.passwd, db_settings.db)
cur = con.cursor()

q = "UPDATE tekijat SET category = %s WHERE role = %s"

with open('role-category.txt') as f:
	for r in f:
		d = r.split('\t')
		if len(d) > 1:
			cur.execute(q, (d[1].rstrip(), d[0]) )
