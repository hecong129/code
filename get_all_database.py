#!/usr/bin/env python

import MySQLdb

host="10.75.19.79"
user="pt"
password="123456"
port="5580"

systemdb_list=['information_schema','test','xddmm','mysql','zjmdmm','performance_schema']

def get_all_tables(conn,db):
	conn=MySQLdb.connect(host=host,user=user,passwd=password,port=int(port),db=db)
	cursor=conn.cursor()
	
	
	cursor.execute("show tables")
	
	result=cursor.fetchall()
	
	for row in result:
		tb=row[0]
		print tb	

	cursor.close()
	conn.close()
	
def get_all_databases():
	conn=MySQLdb.connect(host=host,user=user,passwd=password,port=int(port),charset="utf8")
	
	cursor=conn.cursor()
	
	cursor.execute("show databases")
	
	result=cursor.fetchall()
	
	for row in result:
		db=row[0]
		
		if db not in systemdb_list:
			print_flag="#"*15
			print "%s %s %s" % (print_flag,db,print_flag)
			
			get_all_tables(conn,db)
	cursor.close()
	conn.close()

def main():
	get_all_databases()

if __name__=='__main__':
	main()
