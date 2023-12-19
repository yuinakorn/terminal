#!/usr/bin/env python3.9
import os
import multiprocessing as mp
from subprocess import Popen, PIPE, STDOUT
from optparse import OptionParser
from queue import Queue
from threading import Thread
import mysql.connector
# from progress.bar import Bar
import progressbar

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
parser.add_option("-c","--no-create-info",dest="createinfo",
                  help="add option --no-create-info default set to true",
                  default="true")
parser.add_option("-l","--skip-add-locks",dest="skiplock",
                  help="add option --skip-add-locks default set to true",
                  default="true")
parser.add_option("-a","--auto-commit",dest="autocommit",
                  help="add option --no-auto-commit default set to false",
                  default="false")

parser.add_option("-m","--dump-command",dest="command",
                  help="mysqldump or mariadb-dump",
                  default="mysqldump")

(options, args) = parser.parse_args()

character_set = "tis620"


class Runprogress:

    def __init__(self):
        self.count = 0
        self.bar = None

    def Update(self):
        self.count += 1
        self.bar.update(self.count)
        
    def setmax(self,max):
        self.bar = progressbar.ProgressBar(max_value=max)
        return self.bar
    
bar = Runprogress()
def run(command,tablename):
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    bar.Update()
    if len(output) > 0:
        with open("/tmp/dump.txt", "a") as myfile:
            myfile.write(output + " : " + tablename )

def worker(queue):
    for args in iter(queue.get, None):
        try:
            run(*args)
        except Exception as e:  # catch exceptions to avoid exiting the
            # thread prematurely
            print("",end="")

def read_table():
    q = Queue()
    conn = mysql.connector.connect (user=mysql_user, password=mysql_pwd,host=mysql_host,buffered=True,database=mysql_db,port=mysql_port)
    cursor = conn.cursor()
    command = "select TABLE_NAME from information_schema.`TABLES` where TABLE_SCHEMA='%s';" %(mysql_db)
    cursor.execute(command)
    maxrow = cursor.rowcount
    records = cursor.fetchall()
    bar.setmax(maxrow)
    for row in records:
        command = "%s -h %s -u %s -p%s --default-character-set=%s --lock-tables=false --complete-insert --extended-insert=true " %(mysql_command,mysql_host,mysql_user,mysql_pwd,character_set)
        
        if options.createinfo == "true" : 
            command += " --no-create-info "
        else:
            command += " --add-drop-table "
        if options.skiplock == "true" :
            command += " --skip-add-locks "
        if options.autocommit == "false" :
            command += " --no-autocommit "

        command +=  " -P %s %s %s  > %s.sql" %(mysql_port,mysql_db,row[0],row[0])
        #print(command)
        q.put_nowait((command,row[0]))

    cursor.close()
    conn.close()
    threads = [Thread(target=worker, args=(q,)) for _ in range(10)]
    for t in threads:
        t.daemon = True  # threads die if the program dies
        t.start()

    for _ in threads: q.put_nowait(None)  # signal no more files
    for t in threads: t.join()  # wait for completion

def show_error():
    print("Fast Mysql Dump Developer By Manop Boonjamnian.\n")
    print ("requice option -i [--ip]                Ip address jhcis server for connect. { Request ! }")
    print ("               -u [--username]          Username login to jhcis server. default set to [root]")
    print ("               -p [--password]          Password to use when connecting to server. default set to [123456]")
    print ("               -P [--port]              Port number to use for connection. defalut set to [3333]")
    print ("               -b [--database]          Database Name. default set to [jhcisdb]")
    print ("               -c [--no-create-info]    add option --no-create-info default set to true")
    print ("               -l [--skip-add-locks]    add options --skip-add-locks default set to true")
    print ("               -a [--auto-commit]       add option --no-auto-commit default set to false")
    print ("               -m [--dump-command]      mysqldump or mariadb-dump")

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
    global mysql_command
    global rowcount 
    rowcount = 0
    mysql_host = options.ipaddress
    mysql_user = options.username
    mysql_pwd = options.password
    mysql_db = options.database
    mysql_port = options.port
    mysql_command = options.command
    return "True"

if __name__ == "__main__" :
    if check_option() == "True" and setoptions() == "True" :
        mp.freeze_support()
        print("Fast Mysql Dump Developer By Manop Boonjamnian.\n")
        read_table()
