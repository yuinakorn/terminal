#!/usr/bin/env python3.9
import os
import multiprocessing as mp
from subprocess import Popen, PIPE, STDOUT
from optparse import OptionParser
from queue import Queue
from threading import Thread
import progressbar

parser = OptionParser()

parser.add_option("-d","--dir_sql", dest="path",help="path to *.sql ")
parser.add_option("-i","--ip",dest="ipaddress",
                  help="Ip address jhcis server.")
parser.add_option("-u","--user",dest="username",
                  help="User for login if not current user.",
                  default="root")
parser.add_option("-p","--password",dest="password",
                  help="Password to use when connecting to server. If password is not given it's asked from the tty.",
                  default="123456")
parser.add_option("-P","--port",dest="port",
                  help="Port number to use for connection.",
                  default="3333")
parser.add_option("-b","--database",dest="database",
                  help="Data Base name default set to \"jhcisdb\"",
                  default="jhcisdb")
parser.add_option("-c","--command",dest="command",
                  help="mysql or mariadb import commmand",
                  default="mysql")

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

def run(command,filename):
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    bar.Update()
    #os.remove(filename)
    if len(output) > 0:
        with open("/tmp/err.txt", "a") as myfile:
            myfile.write(output +" : " + filename + " \n" )

def worker(queue):
    for args in iter(queue.get, None):
        try:
            run(*args)
        except Exception as e:  # catch exceptions to avoid exiting the
            # thread prematurely
            print("",end="")

def start_process():
    q = Queue()
    count = 0
    for file in os.listdir(backupdir):
        if file.endswith(".sql"):
            command = "%s -h %s -u %s -p%s -P %s -f --default-character-set=%s  %s < %s" %(options.command,mysql_host,mysql_user,mysql_pwd,mysql_port,character_set,mysql_db,backupdir + file )
            print(command)
            q.put_nowait((command, file))
            count += 1

    bar.setmax(count)

    threads = [Thread(target=worker, args=(q,)) for _ in range(100)]
    for t in threads:
        t.daemon = True  # threads die if the program dies
        t.start()

    for _ in threads: q.put_nowait(None)  # signal no more files
    for t in threads: t.join()  # wait for completion

def show_error():
    print ("requice option -i [--ip]        Ip address jhcis server for connect. { Request ! }")
    print ("               -d [--dir_sql]   Path to *.sql { Request ! }")
    print ("               -u [--username]  Username login to jhcis server. default set to [root]")
    print ("               -p [--password]  Password to use when connecting to server. default set to [123456]")
    print ("               -P [--port]      Port number to use for connection. defalut set to [3333]")
    print ("               -b [--database]  Database Name. default set to [jhcisdb]")
    print ("               -c [--command]   mysql or mariadb command for import")

def check_option():
    if options.path == None or options.ipaddress == None :
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
    global rowcount
    rowcount = 0
    backupdir = options.path
    mysql_host = options.ipaddress
    mysql_user = options.username
    mysql_pwd = options.password
    mysql_db = options.database
    mysql_port = options.port
    return "True"

if __name__ == "__main__" :

    if check_option() == "True" and setoptions() == "True" :
        mp.freeze_support()
        print("Fast Mysql Import Developer By Manop Boonjamnian.\n")
        start_process()
