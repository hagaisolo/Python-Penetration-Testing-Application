# This is a ping test, just for checking
import os
import pickle


def ping(ip, data_log_file, count=1):
    hostname = ip
    num = int(count)
    response = os.system("ping -n" + " %s " % num + hostname + " > Temp_Ping")
    f = open("Temp_Ping", 'r')
    data_log_file.write(f.read())
    f.close()
    if response == 0:
        data_log_file.write("%s is UP!\n" % hostname)
    else:
        data_log_file.write("%s is DOWN!\n" % hostname)


def collect_param():
    # param_file = open('../parameters', 'rb')   # for debug purposes
    param_file = open('Groups//parameters', 'rb')
    param_list = pickle.load(param_file)
    param_file.close()
    return param_list

if __name__ == "__main__":
    data_log_file = open("Groups//Ping//data_log" , 'w')
    data_log_file.write("Hello World This is Ping test")
    parameters = collect_param()
    ping(ip=parameters[0][1], count=parameters[1][1], data_log_file=data_log_file)
    data_log_file.write("Ping Test proccess is Finished")
    data_log_file.close()


