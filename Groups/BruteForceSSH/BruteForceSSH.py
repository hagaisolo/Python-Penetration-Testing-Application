# This is an empty test for demonstration of the application work flow
import paramiko
import socket
import pickle
import threading
import sys
import datetime
import csv
import time

lock = threading.Lock()
attempts = 0

def read_csv(_file='Groups//BruteForceSSH//usernames_temp.csv'):
    filename = (_file)
    f = open(filename, 'rb')
    reader = csv.reader(f)
    try:
        user_list = []
        for row in reader:
            user_list.extend(row)
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
    return user_list


class SSHForce(threading.Thread):
    def __init__(self, _ip, _port, _username, _passwords=True):
        threading.Thread.__init__(self)
        paramiko.util.log_to_file("Groups//BruteForceSSH//paramiko.log")
        self.IP = _ip
        self.PORT = _port
        self.username = _username
        self.passwords = _passwords
        # assign a name to the thread for better debug
        name = ("Thread %s" % attempts)
        threading.current_thread().setName(name)
        self.id = threading.current_thread().getName()

        self.ret = [0, 0]

    def guess_ssh_user(self, _password=''):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.IP, username=self.username, password=_password)
            lock.acquire()
            print ("###############Succeed Login############# - password is: %s   ,  user name is:%s" % (_password, self.username))
            lock.release()
            client.close()
            self.ret = ['Success', self.username]
        except socket.error as e:
            lock.acquire()
            print ("Error on Thread: %s" % self.id)
            print "Socket Error"
            print e
            print ("\n")
            lock.release()
        except paramiko.AuthenticationException as e:
            lock.acquire()
            print ("Failed to Login - password is not %s for user name ==> %s" % (_password, self.username))
            print e
            lock.release()
        except paramiko.SSHException as e:
            lock.acquire()
            print ("Error on Thread: %s User name: %s" % (self.id, self.username)), '\n', e
            lock.release()
            time.sleep(3)
            del client
            self.guess_ssh_user()

    def join(self, timeout=None):
        threading.Thread.join(self)
        return self.ret

    def run(self):
        if not self.passwords:
            self.guess_ssh_user()
        else:
            passwords = read_csv('Groups//BruteForceSSH//password_temp.csv')
            for password in passwords:
                self.guess_ssh_user(password)


def collect_param():
    # param_file = open('../parameters', 'rb')   # for debug purposes
    param_file = open('Groups//parameters', 'rb')
    param_list = pickle.load(param_file)
    param_file.close()
    return param_list


if __name__ == "__main__":

    # initiating variable and log files
    data_log = open("Groups//BruteForceSSH//data_log", 'w')
    temp_stdout = sys.stdout
    sys.stdout = data_log
    success = False
    UserList = read_csv()

    print "BruteForceGroup"
    print ("Test run on: %s" % datetime.datetime.utcnow())

    parameters = collect_param()
    # parsed_parameters_main = parse_param(parameters)
    print "Parsed Successfully"

    # Checking Root login
    print "Testing if root login is enable:"
    root_test = SSHForce(_ip=parameters['ip'],
                      _port=parameters['port'],
                      _username="root",
                         _passwords=False)
    root_test.start()

    # Testing for users with empty passwords
    th = ['']*len(UserList)
    for i in range(0, len(UserList)):
        # th[i] = threading.Thread(target=thread_routine, args=(parsed_parameters_main, UserList[i]))
        th[i] = SSHForce(_ip=parameters['ip'],
                      _port=parameters['port'],
                      _username=UserList[i],
                         _passwords=False)
        th[i].start()
        attempts += 1
        if threading.active_count() > 99:
            time.sleep(10)
        time.sleep(0.1)

    # join threads
    for t in th:
        return_value = t.join()
        if return_value[0] is "Success":
            success = True
            print ("Penetration succeeded, user name is: %s" % return_value[1])
        else:
            pass

    # printing test results
    print ("Tried %s user names with empty password" % attempts)

    # running user name with passwords
    print (" Trying user names with passwords")
    for i in range(0, len(UserList)):
           th[i] = SSHForce(_ip=parameters['ip'],
                         _port=parameters['port'],
                         _username=UserList[i],
                            _passwords=True)
           th[i].start()
           attempts += 1
           if threading.active_count() > 99:
               time.sleep(10)
           time.sleep(0.1)

    # join threads
    for t in th:
        return_value = t.join()
        if return_value[0] is "Success":
            success = True
            print ("Penetration succeeded, user name is: %s" % return_value[1])
        else:
            pass

    print ("Finish user with password testing")
    print ("Test end at %s" % datetime.datetime.utcnow())
    user_amount = len(UserList)
    pass_amount = len(read_csv('Groups//BruteForceSSH//password_temp.csv'))
    print ("Tested %s user names with %s passwords each" %(user_amount, pass_amount))
    # closing files and etc
    sys.stdout = temp_stdout
    data_log.close()
