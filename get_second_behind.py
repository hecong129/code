#!/usr/bin/env python

import MySQLdb
import time

class Get_second_behind():


	def __init__(self,host,user,password,port,rep_user):
		self.host=host
		self.user=user
		self.password=password
		self.port=int(port)
		self.db="test"
		self.rep_user=rep_user
		self.slaves_list=[]
		self.lags=[]

	def get_slaves(self):
		conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,port=self.port,db=self.db)
		
		cursor=conn.cursor()
		cursor.execute("show processlist")
		
		result=cursor.fetchall()
		for row in result:
			pro_user=row[1]
			if pro_user == self.rep_user:
				slave_ip=row[2].split(':')[0]
				self.slaves_list.append(slave_ip)
		
		cursor.close()
		conn.close()

	def print_slaves(self):

		lag_file=open("3875_lag",'a')
		length=len(self.slaves_list)
		now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
		message="%s %s %s" % ('-'*10,now,'-'*10)
		print message
		lag_file.write(message+"\n")

		for i in range(length):
			message="%-20s %d" % (self.slaves_list[i],self.lags[i])
			print message
			lag_file.write(message+"\n")
		lag_file.close()
	
	def get_all_slave_lag(self):
		
		for slave in self.slaves_list:
			conn=MySQLdb.connect(host=slave,user=self.user,passwd=self.password,port=self.port,db=self.db)
			cursor=conn.cursor()


			cursor.execute("show slave status")
		
			result=cursor.fetchall()
		
			for row in result:
				self.lags.append(row[32])

			cursor.close()
			conn.close()
	

def main():
    host="10.73.18.55"
    user="superdba"
    password="DS4anis@ABDx"
    port="3875"
    rep_user="replica"


    gsh=Get_second_behind(host,user,password,port,rep_user)
    gsh.get_slaves()

    gsh.get_all_slave_lag()
    gsh.print_slaves()

if __name__=="__main__":
	main()
