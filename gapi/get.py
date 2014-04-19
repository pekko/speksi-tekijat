# coding: utf-8

import os

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2

import xml.etree.ElementTree as ET
import csv
import StringIO
import MySQLdb

class Tekijat(object):
	def __init__(self):
		CREDENTIALS_FILENAME = '.credentials'

		if not os.path.isfile(CREDENTIALS_FILENAME):
			flow = OAuth2WebServerFlow(client_id='452665123375.apps.googleusercontent.com',
									   client_secret='odA1qIM7a2wV9tqflieF7k_Z',
									   scope='https://spreadsheets.google.com/feeds',
									   redirect_uri='http://localhost')

			auth_uri = flow.step1_get_authorize_url()
			print auth_uri

			code = '4/VxEGacqWScdA6XbV-3lePdaC9AiR.kuGt6o4KeRcYYKs_1NgQtmVnMiLyigI'
			credentials = flow.step2_exchange(code)
			storage = Storage(CREDENTIALS_FILENAME)
			storage.put(credentials)

		else:
			storage = Storage(CREDENTIALS_FILENAME)
			credentials = storage.get()

		http = httplib2.Http()
		http = credentials.authorize(http)

		self.http = http
		self.db = MySQLdb.connect(host='db1.kapsi.fi', user='pwc', passwd='Tookiko1', db='pwc', charset='utf8')
		self.cur = self.db.cursor()

	def get_urls(self, key):
		(_, xml) = self.http.request('https://spreadsheets.google.com/feeds/worksheets/%s/private/full' % (key), 'GET')
		root = ET.fromstring(xml)
		
		links = {}
		for c in root.findall('{http://www.w3.org/2005/Atom}entry'):
			for x in c.findall('{http://www.w3.org/2005/Atom}link'):
				links[x.attrib['rel']] = x.attrib['href']
		return links

	def update_row(self, id, data):
		args = data + [id]

		return self.cur.execute("""
		UPDATE tekijat 
		SET 
			role = %s,
			category = %s,
			subcat1 = %s,
			subcat2 = %s,
			last_name = %s,
			first_name = %s,
			year = %s
		WHERE id = %s
			""", args)

	def get_csv_url(self, sheetkey):
		urls = self.get_urls(sheetkey)
		csv_url = urls["http://schemas.google.com/spreadsheets/2006#exportcsv"]
		return csv_url

	def update_database(self, csv_url):
		(_, csvdata) = self.http.request(csv_url)
		csvdata = csvdata
		reader = csv.reader(StringIO.StringIO(csvdata))
		
		first_pass = True
		for row in reader:
			if first_pass: 
				first_pass = False
				continue

			self.update_row(int(row[0]), row[1:])


def main():
	t = Tekijat()
	# url = t.get_csv_url('1HhRZ17PncxOuTD43JVZYLxc7CW-tKilsrtmIYGURjZI')
	url = 'https://docs.google.com/spreadsheets/d/1HhRZ17PncxOuTD43JVZYLxc7CW-tKilsrtmIYGURjZI/export?gid=1394595082&format=csv'
	t.update_database(url)

if __name__ == '__main__':
	main()
