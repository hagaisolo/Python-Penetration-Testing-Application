# This is a ping test, just for checking
import os
import pickle


def ping(ip, count=1):
    hostname = ip
    num = int(count)
    response = os.system("ping -n" + " %s " % num + hostname)
    if response == 0:
        print hostname, 'is up!'
    else:
        print hostname, 'is down!'


def collect_param():
    # param_file = open('../parameters', 'rb')   # for debug purposes
    param_file = open('Groups//parameters', 'rb')
    param_list = pickle.load(param_file)
    param_file.close()
    return param_list

if __name__ == "__main__":
    print "Hello World"
    parameters = collect_param()
    ping(ip=parameters[0][1], count=parameters[1][1])
    raw_input("Press any key To exit group")



