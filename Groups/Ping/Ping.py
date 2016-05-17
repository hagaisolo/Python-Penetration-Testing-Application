# This is a ping test, just for checking
import os
from Core.Tools import core_get_parameters
import datetime


def ping(ip, _data_log_file, count=1):
    hostname = ip
    num = int(count)
    response = os.system("ping -n" + " %s " % num + hostname + " > Groups//Ping//Temp_Ping")
    f = open("Groups//Ping//Temp_Ping", 'r')
    _data_log_file.write(f.read())
    f.close()
    if response == 0:
        _data_log_file.write("%s is UP!\n" % hostname)
    else:
        _data_log_file.write("%s is DOWN!\n" % hostname)


if __name__ == "__main__":
    data_log_file = open("Groups//Ping//data_log", 'w')
    data_log_file.write("Hello World This is Ping test\n")
    data_log_file.write("Test run at: %s\n" % datetime.datetime.utcnow())
    parameters = core_get_parameters.core_get_parameters()
    ping(ip=parameters[0][1], count=parameters[1][1], _data_log_file=data_log_file)
    data_log_file.write("Ping Test proccess is Finished")
    data_log_file.close()


