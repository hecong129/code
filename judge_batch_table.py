#!/usr/bin/env python2.7

import os
import sys
from optparse import OptionParser

def usage():
        usage='''usage:
        ./judge_batch_table.py -P port
        '''
        print usage


def main():

        if len(sys.argv)==1:
                usage()
        else:
                parser=OptionParser()
                parser.add_option("-P","--Port",action="store",dest="port")

                (option,args)=parser.parse_args(sys.argv)

                ip_list=[]

                cmd="dbdig.sh %s" % option.port
                print "Get all iplist of %s..." % option.port

                dbdig_output=os.popen(cmd).readlines()

                for line in dbdig_output:
                        if '10' in line:
                                ip=line.split()[3]
                                print ip
                #os.system('./judge_table.py -H 127.0.0.1 -upt -p123456 -P 5580 -d sakila -t my_data -c rank')

if __name__ == '__main__':
        main()
~                
