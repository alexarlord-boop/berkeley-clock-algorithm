import random
import socket
import time

import settings
from utilities.logging import SynchronizedPrinter


class Node(SynchronizedPrinter):
    def __init__(self, port, tag, time_bias):
        super().__init__()
        self.port = port
        self.time_bias = time_bias  # equals 0 if master
        self.tag = tag
        self.is_master = False
        self.is_alive = True
        self.time_to_live = 10

    def run(self):
        if self.is_master:
            self.master_run()
        else:
            self.slave_run()

    def master_run(self):
        self.print_message(f"master {self.tag} started.")
        while self.is_alive and self.time_to_live > 0:
            time.sleep(1)
            # self.synchronize_clocks()

    def slave_run(self):
        self.print_message(f"slave {self.tag} started.")
        while self.is_alive and self.time_to_live > 0:
            time.sleep(1)
            # self.synchronize_clocks()
            if random.random() < 0.2:  # Simulate node failure with 20% probability
                # self.print_message(f"{self.tag} failed.")
                self.stop()

    def stop(self):
        self.is_alive = False
        self.print_message(f"{self.tag} stopped.")

    # def synchronize_clocks(self):
    #     if self.is_master:
    #         self.broadcast_time_request()
    #     else:
    #         self.send_time_request()
    #
    # def broadcast_time_request(self):
    #     response = f'SET_TIME,{self.tag},{self.time_bias}'
    #     self.broadcast(response)
    #
    # def send_time_request(self):
    #     response = 'TIME_REQUEST'
    #     self.send_message(self, response)
    #
    # def send_message(self, target, message):
    #     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     client_socket.connect(('localhost', target.port))
    #     client_socket.send(message.encode('utf-8'))
    #     client_socket.close()