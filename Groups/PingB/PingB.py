# This is a tcp flood group , for checking core

from Core.features import features
import time
import datetime

if __name__ == "__main__":
	main()

def main():
    print ("This the PingB group")
    parameters = features.core_get_parameters()
    print parameters
    data_log_file = open("Groups//PingB//data_log", 'w')
    data_log_file.write("Just Do Nothing\n")
    data_log_file.write("Test run at: %s\n" % datetime.datetime.utcnow())
    time.sleep(5)
    data_log_file.write("Test proccess is Finished")
    data_log_file.close()


