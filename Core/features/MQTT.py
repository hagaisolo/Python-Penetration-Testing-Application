#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MQTT V3.1.1 protocol feature
"""
from uuid import getnode as get_mac
import socket
import struct
from threading import Lock

safe_print = Lock


Debug = False

MQTTv31 = 3
MQTTv311 = 4

PROTOCOLS = ["zero", "a", "b", "MQIsdp", "MQTT"]

MessageTypes = dict()
MessageTypes["CONNECT"] = 0x10
MessageTypes["CONNACK"] = 0x20
MessageTypes["PUBLISH"] = 0x30
MessageTypes["PUBACK"]  = 0x40
MessageTypes["PUBREC"]  = 0x50
MessageTypes["PUBREL"]  = 0x60

"""
ConnackCode = dict()
ConnackCode["CONNACK_ACCEPTED"] = 0
ConnackCode["CONNACK_REFUSED_PROTOCOL_VERSION"] = 1
ConnackCode["CONNACK_REFUSED_IDENTIFIER_REJECTED"] = 2
ConnackCode["CONNACK_REFUSED_SERVER_UNAVAILABLE"] = 3
ConnackCode["CONNACK_REFUSED_BAD_USERNAME_PASSWORD"] = 4
ConnackCode["CONNACK_REFUSED_NOT_AUTHORIZED"] = 5
"""

ConnackCode = ["CONNACK_ACCEPTED","CONNACK_REFUSED_PROTOCOL_VERSION","CONNACK_REFUSED_IDENTIFIER_REJECTED",
               "CONNACK_REFUSED_SERVER_UNAVAILABLE", "CONNACK_REFUSED_BAD_USERNAME_PASSWORD",
               "CONNACK_REFUSED_NOT_AUTHORIZED"]

"""
This is stright forward version of connect message to help debug
# description      flags len     prolen     M      Q     T    T    level flag time   time ID msb  lsb   T   T
connect_message = [0x10, 0x0E, 0x00, 0x04, 0x4D, 0x51, 0x54, 0x54, 0x04, 0x00, 0x00, 0x0A, 0x00, 0x02, 0x54, 0x54]
connect_packet = bytearray(connect_message)
"""


class Message(object):
    """
    Each message is a dictionary for easy access and manipulation of packet
    it uses get_packet method to get a buffer from the dictionary
    """
    def __init__(self):
        self.fixed_header = dict()
        self.variable_header = dict()
        self.payload = dict()

        self.variable_header_flag = False
        self.payload_flag = False

        # Fixed Header
        # bytes
        self.fixed_header["Remaining Length"] = 0

    @staticmethod
    def encode_string_to_bytes(_str):
        length = len(_str)
        msb = ((length >> 8) % 256)
        lsb = (length % 256)
        buffer_bytes = [msb,lsb]
        for char in _str:
            buffer_bytes += [ord(char)]
        return buffer_bytes

    @staticmethod
    def encode_variable_length(_x):
        remaining_length_bytes = []
        x = _x
        encode_byte = x % 128
        x /= 128
        if x > 0:
            encode_byte |= 128
        remaining_length_bytes += [encode_byte]
        while x > 0:
            encode_byte = x % 128
            x /= 128
            if x > 0:
                encode_byte |= 128
            remaining_length_bytes += [encode_byte]
        return remaining_length_bytes

    @staticmethod
    def decode_variable_length(_digits):
        multiplier = 1
        value = 0
        for digit in _digits:
            value += (digit & 127) * multiplier
            multiplier *= 128


class ConnectMessage(Message):
    def __init__(self, _protocol, _id):
        Message.__init__(self)
        self.variable_header_flag = True
        self.payload_flag = True

        # byte 1
        self.fixed_header["Message Type"] = 1
        self.fixed_header["DUP Flag"] = 0
        self.fixed_header["QoS Level"] = 0
        self.fixed_header["Retain"] = 0
        # byte 2
        self.fixed_header["Remaining Length"] = 0xE
        # Variable Header part
        # bytes
        self.variable_header["ProtocolName"] = _protocol
        # bytes
        self.variable_header["Level"] = 4
        # bytes
        self.variable_header["CleanSession"] = 0
        self.variable_header["WillFlag"] = 0
        self.variable_header["WillQoS"] = 0
        self.variable_header["WillRetain"] = 0
        self.variable_header["PasswordFlag"] = 0
        self.variable_header["UserNameFlag"] = 0
        # bytes
        self.variable_header["KeepAlive"] = 10

        # PayLoad part
        # bytes
        self.payload["ClientID"] = _id
        # bytes
        self.payload["WillTopic"] = u"test"
        # bytes
        self.payload["WillMessage"] = u"test"
        # bytes
        self.payload["UserName"] = u"user"
        # bytes
        self.payload["PassWord"] = u"pass"

    def get_packet(self):
            packet = []
            # getting Fixed Header bytes
            buffer_fixed_header = [(self.fixed_header["Retain"]+self.fixed_header["QoS Level"]*2
                                       + self.fixed_header["DUP Flag"]*8 + self.fixed_header["Message Type"]*16)]
            buffer_fixed_header += self.encode_variable_length(_x=self.fixed_header["Remaining Length"])

            packet += buffer_fixed_header
            # part for variable header if it exists
            if self.variable_header_flag:
                buffer_variable_header = self.encode_string_to_bytes(self.variable_header["ProtocolName"])
                buffer_variable_header += [(self.variable_header["Level"])]
                byte8 = (self.variable_header["CleanSession"]*2 + self.variable_header["WillFlag"]*4 +
                            self.variable_header["WillQoS"]*8 + self.variable_header["WillRetain"]*32 +
                            self.variable_header["PasswordFlag"]*64 + self.variable_header["UserNameFlag"]*128)
                buffer_variable_header += [(byte8)]
                keep_alive_msb = (self.variable_header["KeepAlive"] >> 8)
                keep_alive_lsb = (self.variable_header["KeepAlive"] % 256)
                buffer_variable_header += [keep_alive_msb]
                buffer_variable_header += [keep_alive_lsb]

                packet += buffer_variable_header

            if self.payload_flag:
                buffer_payload = self.encode_string_to_bytes(self.payload["ClientID"])
                if self.variable_header["WillFlag"] == 1:
                    buffer_payload += (self.encode_string_to_bytes(self.payload["WillTopic"]))
                    buffer_payload += (self.encode_string_to_bytes(self.payload["WillMessage"]))
                if self.variable_header["UserNameFlag"] == 1:
                    buffer_payload += (self.encode_string_to_bytes(self.payload["UserName"]))
                if self.variable_header["PasswordFlag"] == 1:
                    buffer_payload += (self.encode_string_to_bytes(self.payload["PassWord"]))

                # packet.extend(struct.pack("!H", len(buffer_payload)))
                packet += buffer_payload

            return bytearray(packet)


class DisconnectMessage(Message):
    def __init__(self):
        Message.__init__(self)
        self.fixed_header["Message Type"] = 14
        self.variable_header_flag = False
        self.payload_flag = False
        self.fixed_header["Remaining Length"] = 0x00

    def get_packet(self):
        packet = []
        packet += [self.fixed_header["Message Type"]*16]
        packet += [self.fixed_header["Remaining Length"]]
        return bytearray(packet)


class PublishMessage(Message):
    def __init__(self):
        Message.__init__(self)
        self.variable_header_flag = True
        self.payload_flag = True
        # Fixed Header
        # byte 1
        self.fixed_header["Retain"] = 0
        self.fixed_header["DUP Flag"] = 0
        self.fixed_header["Message Type"] = 3
        self.fixed_header["QoS Level"] = 1

        self.variable_header["PacketID"] = [0,0]
        self.variable_header["TopicName"] = "a/b"
        self.payload["AppData"] = "a"

    def get_packet(self):
        packet = []
        # getting Fixed Header bytes
        buffer_fixed_header = [(self.fixed_header["Retain"]+self.fixed_header["QoS Level"]*2
                                   + self.fixed_header["DUP Flag"]*8 + self.fixed_header["Message Type"]*16)]
        buffer_fixed_header += self.encode_variable_length(_x=self.fixed_header["Remaining Length"])
        packet += buffer_fixed_header
        # part for variable header if it exists
        if self.variable_header_flag:
            buffer_variable_header = self.encode_string_to_bytes(self.variable_header["TopicName"])
            buffer_variable_header += self.variable_header["PacketID"]

            packet += buffer_variable_header

        if self.payload_flag:
            buffer_payload = self.encode_string_to_bytes(self.payload["AppData"])
            packet += buffer_payload

        print packet
        packet[1] = (len(packet)-2)
        return bytearray(packet)


class PubreckMessage(Message, ):
    def __init__(self, _packet_id=[0,0]):
        Message.__init__(self)
        self.variable_header_flag = True
        self.payload_flag = False
        self.fixed_header["Message Type"] = 5
        self.fixed_header["Remaining Length"] = 2

        self.variable_header["PacketID"] = _packet_id

    def get_message(self):
        message = []
        message += [self.fixed_header["Message Type"]*16]
        message += [self.fixed_header["Remaining Length"]]
        message += self.variable_header["PacketID"]
        return message


class PubrelkMessage(Message, ):
    def __init__(self, _packet_id=[0,0]):
        Message.__init__(self)
        self.variable_header_flag = True
        self.payload_flag = False
        self.fixed_header["Message Type"] = 6
        self.fixed_header["Reserved"] = 2
        self.fixed_header["Remaining Length"] = 2

        self.variable_header["PacketID"] = _packet_id

    def get_message(self):
        message = []
        message += [self.fixed_header["Message Type"]*16 + self.fixed_header["Reserved"]]
        message += [self.fixed_header["Remaining Length"]]
        message += self.variable_header["PacketID"]
        return message

    def get_packet(self):
        return bytearray(self.get_message())


class PubcompMessage(Message, ):
    def __init__(self, _packet_id=[0,0]):
        Message.__init__(self)
        self.variable_header_flag = True
        self.payload_flag = False
        self.fixed_header["Message Type"] = 7
        self.fixed_header["Reserved"] = 0
        self.fixed_header["Remaining Length"] = 2

        self.variable_header["PacketID"] = _packet_id

    def get_message(self):
        message = []
        message += [self.fixed_header["Message Type"]*16 + self.fixed_header["Reserved"]]
        message += [self.fixed_header["Remaining Length"]]
        message += self.variable_header["PacketID"]
        return message

    def get_packet(self):
        return bytearray(self.get_message())


class PubackMessage(Message, ):
    def __init__(self, _packet_id=[0,0]):
        Message.__init__(self)
        self.variable_header_flag = True
        self.payload_flag = False
        self.fixed_header["Message Type"] = 4
        self.fixed_header["Remaining Length"] = 2

        self.variable_header["PacketID"] = _packet_id

    def get_message(self):
        message = []
        message += [self.fixed_header["Message Type"]*16]
        message += [self.fixed_header["Remaining Length"]]
        message += self.variable_header["PacketID"]
        return message


class Client(object):
    def __init__(self, _id=get_mac(), _clean_session=True, _userdata=None, _protocol=MQTTv311):
        self.id = _id
        self.address = ("85.119.83.194", 1883)
        self.clean_session = _clean_session
        self.user_data = _userdata
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.protocol = PROTOCOLS[_protocol]

    def connect(self, _address):
        # establish tcp connection with socket
        self.tcp_connect(_address)
        # send CONNECT MQTT packet
        connect_message = ConnectMessage(_protocol=self.protocol ,_id = self.id ).get_packet()
        self.sock.sendall(connect_message)
        # validate connack message
        connack_message = self.get_connack()
        print ConnackCode[connack_message[3]]

    def get_connack(self):
        chunks = []
        for i in range(4):
            chunk = (self.sock.recv(1))
            if chunk == '':
                break
            tmp = struct.unpack('B', chunk)[0]
            chunks.append(tmp)
        return chunks

    def tcp_connect(self, _address):
        """
        wait for a connection to be established via server
        :param: _add a 2-tuple of (IP, PORT)
        :return:
        """
        try:
            self.sock.connect(_address)
            print "Socket connection established"
        except socket.error as e:
            print e
            self.sock.close()

    def disconnect(self):
        """
        Waits for the MQTT client to finish any work it must do, and for the TCP/IP session to disconnect.
        :return:
        """
        # wait ...
        disconnect_message = DisconnectMessage().get_packet()
        self.sock.sendall(disconnect_message)
        self.sock.shutdown(1)
        self.sock.close()
        if Debug:
            print disconnect_message
            print "Disconnected..."

    def subscribe(self):
        """
        Waits for completion of the Subscribe or UnSubscribe method.
        :return:
        """
        pass

    def unsubscribe(self):
        """
        Requests the server unsubscribe the client from one or more topics.
        :return:
        """
        pass

    def publish(self, _message):
        """
        Returns immediately to the application thread after passing the request to the MQTT client.
        :return:
        """
        byte_message = (_message.get_packet())
        self.sock.sendall(byte_message)
        if Debug:
            print "Sent Message"
        if _message.fixed_header["QoS Level"] == 1:
            received_message = self.get_message()
            expected_message = PubackMessage().get_message()
            if Debug:
                print received_message
                print expected_message
        if _message.fixed_header["QoS Level"] == 2:
            """
            QoS Level 2 protocol
            sent publish, receive pubrek, send pubrel receive pubcomp
            """
            received_message = self.get_message()
            expected_message = PubreckMessage().get_message()
            if Debug:
                print received_message
                print expected_message
            if received_message == expected_message:
                pubrel_message = PubrelkMessage(_packet_id= [received_message[2], received_message[3]])
                if Debug:
                    print pubrel_message.get_message()
                byte_message = pubrel_message.get_packet()
                self.sock.sendall(byte_message)

                received_message = self.get_message()
                expected_message = PubcompMessage().get_message()

                if received_message == expected_message:
                    print "QoS level 2 achieved successfull"

    def get_message(self):
        chunks = []
        chunk = ''
        # recieving first byte
        while chunk == '':
            chunk = (self.sock.recv(1))
        tmp = struct.unpack('B', chunk)[0]
        chunks.append(tmp)
        # second byte to find remaining length
        chunk = (self.sock.recv(1))
        tmp = struct.unpack('B', chunk)[0]
        print tmp
        chunks.append(tmp)
        for i in range(tmp):
            chunk = (self.sock.recv(1))
            chunks.append(struct.unpack('B', chunk)[0])
        print chunks
        return chunks

    def listen(self):
        for res in socket.getaddrinfo(None, 1883, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, add = res
            self.listen_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

            try:
                self.listen_sock.bind(("192.168.1.14", 1883))
                self.listen_sock.listen(1)
            except socket.error as msg:
                self.listen_sock.close()
        conn, addr = self.listen_sock.accept()
        print 'Connected by', addr
