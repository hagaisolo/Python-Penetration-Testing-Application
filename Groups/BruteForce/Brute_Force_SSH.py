# This is an empty test for demonstration of the application work flow
# from pexpect import ExceptionPexpect, TIMEOUT, spawn, EOF  # try and fail to use pxshh
# from pexpect import pxssh
import paramiko
import getpass
import pickle
from threading import Thread


class SSHForce(object):
    def __init__(self, _ip, _port):
        self.IP = _ip
        self.PORT = _port
        self.hostname = raw_input('hostname: ')
        self.username = raw_input('username: ')

    def guess_ssh_user(self,low_lim, up_lim):
        try:
            ssh = paramiko.SSHClient()
            password = getpass.getpass('password: ')
            ssh.connect(hostname=self.hostname, username=self.username, password=password)
        except paramiko.SFTPError, e:
            print "Failed to Login"
            print e


def collect_param():
    param_file = open('../parameters', 'rb')   # for debug purposes
    # param_file = open('Groups//parameters', 'rb')
    param_list = pickle.load(param_file)
    param_file.close()
    return param_list


def parse_param(param_list):
    parsed_param = {}
    for item in param_list:
        parsed_param[item[0]] = item[1]
    return parsed_param


def thread_routine(_parsed_parameters_main):
    cannon = SSHForce(_ip=_parsed_parameters_main['_IP'], _port=_parsed_parameters_main['_PORT'])
    cannon.guess_ssh_user()


if __name__ == "__main__":

    # This Group require "pexpect" module
    # The Group require "metakernel" module
    # it also require "getpass" module
    NUM_SSH_FORCE = 100
    print 'GET / HTTP /1.1\r\nHost: google.com\r\n\r\n'
    print "BruteForceGroup"

    parameters = collect_param()
    parsed_parameters_main = parse_param(parameters)
    print "Parsed Successfully"
    # if parsed_parameters_main["_Scapy"]:
    #     scapy_attack(dest_port=["_Port"],dest_ip=parsed_parameters_main["_IP"],src_ip='192.168.1.1', src_port=8080)
    th = ['']*NUM_SSH_FORCE
    for i in range(NUM_SSH_FORCE):
        th[i] = Thread(target=thread_routine, args=(parsed_parameters_main, ))
        th[i].start()