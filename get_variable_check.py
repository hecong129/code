#!/usr/bin/env python
#-*- coding:utf8 -*-

import MySQLdb
import socket
import fcntl
import struct
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

path=""

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def is_on_manger():
    current_ip=get_ip_address('eth1')
    
    if current_ip !='10.55.22.171':
        print "Please run this script on 10.55.22.171[manger machine],for grants"
        exit(1)

def get_group(cursor_manager,instance_cid):
    #获取端口对应的组
    sql_get_group="select dbname from cid2db where cid=%s" % instance_cid
    cursor_manager.execute(sql_get_group)
    group=cursor_manager.fetchone()[0]
    
    return group

def get_cpuint(cursor_manager,instance_cid):
    #获取产品线名称
    sql_get_productname="select name from cpunit where id=%s" % instance_cid
    
    cursor_manager.execute(sql_get_productname) 
    product_name=cursor_manager.fetchone()[0] 
    
    return product_name

def get_port_status(cursor_manager,id):
    sql_port_status="select port_status from nm2domain where nmid=%s" % id
    
    cursor_manager.execute(sql_port_status)
    row=cursor_manager.fetchone()
    
    if row != None:
        port_status=row[0]
    else:
        port_status=5
    return port_status
 
def get_nid(cursor_manager,instance_port,is_mdb_role):
    #获取nid，根据它查找对应的IP
    sql_get_nid=""
    if is_mdb_role: 
         sql_get_nid="select id,nid from node2module where port=%s and mname='mdb'" % instance_port
    else:
        sql_get_nid="select id,nid from node2module where port=%s and mname!='mdb'" % instance_port


    cursor_manager.execute(sql_get_nid)
    
    nid_list=[]
    result=cursor_manager.fetchall()

    for nid_row in result:
        id=nid_row[0]
        nid=nid_row[1]
        port_status=get_port_status(cursor_manager,id)
        
        if is_mdb_role == True and port_status == 1:
            nid_list.append(nid)
        elif is_mdb_role == False:
            nid_list.append(nid)
            
    return nid_list
    
def get_ip_list(cursor_manager,nid_list):
    #根据nodeid查找对应的内网IP
    
    ip_list=[]
    for nid in nid_list:
        sql_get_ip_by_nid="select ip_in from node where id=%s" % nid
        cursor_manager.execute(sql_get_ip_by_nid)
        ip_in=cursor_manager.fetchone()[0] 
        
        ip_list.append(ip_in)
    return ip_list
        

def get_variable_value(ip,port,variable_name):
    user="mysqlha"
    passwd="Jxh2MnxeHw"
    var_value=""
    try: 
        conn=MySQLdb.connect(host=ip,user=user,passwd=passwd,port=int(port))
        
        sql_get_var="show global variables like '%s'" % variable_name
        
        cursor=conn.cursor()
        
        cursor.execute(sql_get_var)
    
        result=cursor.fetchone()
        
        if result !=  None:
              var_value=result[1]
        else:
              var_value="None"
        
        
        cursor.close()
        conn.close()
    except Exception,e:
        print e
        print "ip=%s,port=%s" %(ip,port)
    
    return var_value

def get_variables_withproblem(group,product_name,port,master_ip,slave_ip_list,variable_name,problem_flag):
    
    path="%s_%s.txt" % (group,variable_name)
    
    withproblem_list=[]

    master_var_value=get_variable_value(master_ip,port,variable_name)
    
    if master_var_value.find(problem_flag) != -1:
        withproblem_list.append(master_ip)
    
    slaves_var_values=[]
    
    for slave_ip in slave_ip_list:
        var_value=get_variable_value(slave_ip,port,variable_name) 
        
        if problem_flag in var_value:
            if slave_ip not in withproblem_list:
               withproblem_list.append(slave_ip) 
    
    
    if len(withproblem_list)>0:
        file=open(path,'a')
        message="=======%s=====%s=====\n" %(port,product_name)
        file.write(message)
        for ip in withproblem_list:
            file.write(ip+"\n")
        file.close()

def get_all_iplist(db,variable_name):
    host="m3303i.apollo.grid.sina.com.cn"
    user="mysqlha"
    passwd="Jxh2MnxeHw"
    port=3303
    db=db
    charset="utf8"
    
    #try:
    conn_manager=MySQLdb.connect(host=host,user=user,passwd=passwd,port=port,db=db,charset=charset)
        #查询该产品单端所有端口
    sql_get_alldb_ports="select port,cid from node2module where mname='mdb' limit 100"    
    cursor_manager=conn_manager.cursor()
    cursor_manager.execute(sql_get_alldb_ports)
    reuslt=cursor_manager.fetchall()
        
    for row in reuslt:
        instance_port=row[0]
        instance_cid=row[1]
                    
        group=get_group(cursor_manager,instance_cid)
        product_name=get_cpuint(cursor_manager,instance_cid)
                    
                    #获取主库的nodeid
        nid_list=get_nid(cursor_manager,instance_port,True)
                    #获取主库IP
        master_ip=get_ip_list(cursor_manager,nid_list)[0]         
                    #获取从库的nodeid        
        nid_slave=get_nid(cursor_manager,instance_port,False) 
        slave_ip_list=get_ip_list(cursor_manager,nid_slave)
                    
        get_variables_withproblem(group,product_name,instance_port,master_ip,slave_ip_list,variable_name,problem_flag="max")
                   
    #except Exception,e:
     #   print e
        
    

def main():
    is_on_manger()
    os.system('rm -rf *innodb_data_file_path*')    
    get_all_iplist("nwdp_admin","innodb_data_file_path")

if __name__ == "__main__":
    main()


