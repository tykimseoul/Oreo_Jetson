import json
import socket
from multiprocessing import Process
from PyAccessPoint import pyaccesspoint as ap
from main import *


class Connector:
    def __init__(self):
        self.command_socket = None
        self.host_address = '192.168.123.101'
        self.android_address = None
        self.port = 9999
        self.buffer_size = 128
        self.access_point = ap.AccessPoint(wlan='wlan0', inet='lo0', ssid='jetson', password='oreo')

    def connect(self):
        self.open_socket()
        self.receive_from_android()
        self.stream_to_android()

    def open_socket(self):
        self.access_point.start()
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.command_socket.bind((self.host_address, self.port))
        print("Waiting for client on port %s:%d".format(self.host_address, self.port))

    def receive_from_android(self):
        self.command_socket.settimeout(1)
        command_thread = Process(name='android', target=self.react_to_command)
        command_thread.start()

    def react_to_command(self):
        while True:
            try:
                data_received, address = self.command_socket.recvfrom(self.buffer_size)
                if self.android_address is None:
                    self.android_address = address
                data = json.loads(data_received.decode('utf8'))
                command = (data['selfDrive'], (data['steerAngle'], data['speed']))
                push_command(command)
            except socket.timeout:
                print('timeout')

    def stream_to_android(self):
        pass
