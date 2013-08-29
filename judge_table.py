#!/usr/bin/env python2.7
import MySQLdb
import sys
from optparse import OptionParser

global host,user,password,port,table,new_column,db

def usage():
	usage_meg='''
Usage: judge_table.py [options]

Options:
  -h, 	 	 --help       		show this help message and exit
  -H HOST, 	 --host=HOST  		connect to host
  -u USER,       --user=USER  		user for login
  -p PASSWORD,   --password=PASSWORD 	password for connection
  -P PORT,       --port=PORT  		port number for connection
  -d Database,   --database=Database   	database
  -t TABLE,      --table_tag=TABLE   	table alterd
  -c COLUMN,     --new_column=COLUMN 	new column added'''
	print usage_meg

def init(args):
	global host,user,password,port,table,new_column,db
	parser=OptionParser()
	parser.add_option("-H","--host",help="connect to host",action="store",dest="host")
	parser.add_option("-u","--user",help="user for login",action="store",dest="user")
	parser.add_option("-p","--password",help="password for connection",action="store",dest="password")
	parser.add_option("-P","--port",dest="port",help="port number for connection",action="store")
	parser.add_option("-d","--database",dest="db",help="table alterd",action="store")
	parser.add_option("-t","--table_tag",dest="table",help="table alterd",action="store")
	parser.add_option("-c","--new_column",dest="column",help="new column added",action="store")

	(options,args)=parser.parse_args(args)
	
	host=options.host
	user=options.user
	password=options.password
	port=options.port
	table=options.table
	new_column=options.column
	db=options.db
	
	no_None_Flag=True
	
	if host==" " or host==None:
		print "host is empty"
		no_None_Flag=False
	elif user==" "or user==None:
		print "user is empty"
		no_None_Flag=False
	elif password==" " or password==None:
		print "password is empty"
		no_None_Flag=False
	elif port==" " or port==None:
		print "port is empty"
		no_None_Flag=False
	elif db==" " or db==None:
		print "db is  empty"
		no_None_Flag=False
	elif table==" " or table==None:
		print "table is empty"
		no_None_Flag=False
	elif new_column==" " or new_column==None:
		print "new is empty"
		no_None_Flag=False
	if  no_None_Flag != True:
		sys.exit(1)

def get_tables():
	global host,user,password,port,table,new_column,db


	conn=MySQLdb.connect(host=host,user=user,passwd=password,port=int(port),db=db)

	cursor=conn.cursor()

	cursor.execute("show tables")

	result=cursor.fetchall()
	
	new_column_nums=0

	for row in result:
		tb=row[0]
		if table in tb:
			cursor.execute("show create table %s" %tb)
			
			k_result=cursor.fetchall()
			for k_row in k_result:
				tb_struct=k_row[1]
				if new_column in tb_struct:
					
					new_column_nums=new_column_nums+1			
	
	print "%s %s %s" % ('-'*20,host,'-'*20)
	print new_column_nums
	cursor.close()
	conn.close()


def  main():

	if len(sys.argv) == 1:
		usage()
	else:
		init(sys.argv)
	
		get_tables()

if __name__=="__main__":
	main()
		
