#!/usr/bin/env python3.9
import os
import multiprocessing as mp
from subprocess import Popen, PIPE, STDOUT
from optparse import OptionParser
from queue import Queue
from threading import Thread
import mysql.connector

from mysql.connector.connection import MySQLConnection

parser = OptionParser()
parser.add_option("-i","--ip",dest="ipaddress",
                  help="Ip address Hosxp Master. server.")
parser.add_option("-u","--user",dest="username",
                  help="User for login if not current user.",
                  default="")
parser.add_option("-p","--password",dest="password",
                  help="Password to use when connecting to server. If password is not given it's asked from the tty.",
                  default="")
parser.add_option("-P","--port",dest="port",
                  help="Port number to use for connection.",
                  default="3306")
parser.add_option("-b","--database",dest="database",
                  help="Data Base name default set to \"hdc\"",
                  default="hos")

(options, args) = parser.parse_args()

character_set = "tis620"

def run(command,filename):
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    if len(output) > 0:
        with open("/tmp/dump.txt", "a") as myfile:
            myfile.write(output + " : " + filename )

def worker(queue):
    for args in iter(queue.get, None):
        try:
            run(*args)
        except Exception as e:  # catch exceptions to avoid exiting the
            # thread prematurely
            print("Error ... ")


def read_table():
    q = Queue()
    conn = mysql.connector.connect (user=mysql_user, password=mysql_pwd,host=mysql_host,buffered=True,database=mysql_db)
    cursor = conn.cursor()
    cursor.execute("select TABLE_NAME from information_schema.`TABLES` where TABLE_SCHEMA='hos';")
    records = cursor.fetchall()
    for row in records:
        command = "mysqldump -h %s -u %s -p%s --default-character-set=%s -d --compact --add-drop-table --skip-lock-tables --extended-insert=true -P %s %s %s > %s.sql" %(mysql_host,mysql_user,mysql_pwd,character_set,mysql_port,mysql_db,row[0],row[0])
        q.put_nowait((command,row[0]))
    cursor.close()
    conn.close()
    threads = [Thread(target=worker, args=(q,)) for _ in range(20)]
    for t in threads:
        t.daemon = True  # threads die if the program dies
        t.start()

    for _ in threads: q.put_nowait(None)  # signal no more files
    for t in threads: t.join()  # wait for completion

def show_error():
    print ("requice option -i [--ip]        Ip address jhcis server for connect. { Request ! }")
    print ("               -u [--username]  Username login to jhcis server. default set to [root]")
    print ("               -p [--password]  Password to use when connecting to server. default set to [123456]")
    print ("               -P [--port]      Port number to use for connection. defalut set to [3333]")
    print ("               -b [--database]  Database Name. default set to [jhcisdb]")

def check_option():
    if options.ipaddress == None :
        show_error()
        parser.error("")
        return "False"
    return "True"

def setoptions():
    global backupdir
    global mysql_host
    global mysql_user
    global mysql_pwd
    global mysql_db
    global mysql_port
    global fname
    mysql_host = options.ipaddress
    mysql_user = options.username
    mysql_pwd = options.password
    mysql_db = options.database
    mysql_port = options.port
    return "True"

if __name__ == "__main__" :
    if check_option() == "True" and setoptions() == "True" :
        mp.freeze_support()
        read_table()

