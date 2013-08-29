#!/usr/bin/env python2.7
import MySQLdb
import sys
from optparse import OptionParser

host=""
user=""
password=""
port=0
table=""
new_column=""

def usage():
	usage='''
Usage: judge_table.py [options]

Options:
  -h, 	 	 --help       		show this help message and exit
  -H HOST, 	 --host=HOST  		connect to host
  -u USER,       --user=USER  		user for login
  -p PASSWORD,   --password=PASSWORD 	password for connection
  -P PORT,       --port=PORT  		port number for connection
  -t TABLE,      --table_tag=TABLE   	table alterd
  -c COLUMN,     --new_column=COLUMN 	new column added'''
	print usage

def init(args):
	parser=OptionParser()
	parser.add_option("-H","--host",help="connect to host",action="store",dest="host")
	parser.add_option("-u","--user",help="user for login",action="store",dest="user")
	parser.add_option("-p","--password",help="password for connection",action="store",dest="password")
	parser.add_option("-P","--port",dest="port",help="port number for connection",action="store")
	parser.add_option("-t","--table_tag",dest="table",help="table alterd",action="store")
	parser.add_option("-c","--new_column",dest="column",help="new column added",action="store")

	(options,args)=parser.parse_args(args)

	host=options.host
	user=options.user
	password=options.password
	port=options.port
	table=options.table
	new_column=options.column

	print options.password
def get_tables():
	conn=MySQLdb.connect(host=host,user=user,passwd=password,port=port,db=db)

	cursor=conn.cursor()
	com_sql="use %s;show tables;" % db
	cursor.execute(com_sql)

	result=cursor.fetchall()
	for row in result:
		print row

	cursor.close()
	conn.close()


def  main():

	if len(sys.argv) == 1:
		usage()
	else:
		init(sys.argv)

if __name__=="__main__":
	main()
		
