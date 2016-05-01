# This is an empty test for demonstration of the application work flow
# from pexpect import ExceptionPexpect, TIMEOUT, spawn, EOF  # try and fail to use pxshh
# from pexpect import pxssh
import paramiko
import socket
import pickle
import threading

lock = threading.Lock()


class SSHForce(threading.Thread):
    def __init__(self, _ip, _port, _hostname, _username):
        self.IP = _ip
        self.PORT = _port
        self.hostname = _hostname
        self.username = _username
        self.id = threading.current_thread().ident

    def guess_ssh_user(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.hostname, username=self.username, password="1234")
            client.close()
        except socket.error as e:
            lock.acquire()
            print ("Error on Thread: %s" % self.id)
            print "Socket Error"
            print e
            print ("\n")
            lock.release()
        except paramiko.BadAuthenticationType as e:
            lock.acquire()
            print ("Failed to Login - user name is not ==> %s" % self.username)
            print e
            lock.release()


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


def thread_routine(_parsed_parameters_main, _username):
    cannon = SSHForce(_ip=_parsed_parameters_main['_IP'],
                      _port=_parsed_parameters_main['_Port'],
                      _hostname=_parsed_parameters_main['_Hostname'],
                      _username=_username)
    cannon.guess_ssh_user()


if __name__ == "__main__":

    # This Group require "pexpect" module
    # The Group require "metakernel" module
    # it also require "getpass" module
    NUM_SSH_FORCE = 4
    print 'GET / HTTP /1.1\r\nHost: google.com\r\n\r\n'
    print "BruteForceGroup"

    parameters = collect_param()
    parsed_parameters_main = parse_param(parameters)
    print "Parsed Successfully"
    th = ['']*NUM_SSH_FORCE
    UserList = ["root","yo","sammy","galileo"]
    for i in range(0,NUM_SSH_FORCE):
        th[i] = threading.Thread(target=thread_routine, args=(parsed_parameters_main, UserList[i]))
        th[i].start()
    thread_list =[]
    for t in th:
        t.join()
    print ("Test Finished")
    raw_input("Press any key to continue")
