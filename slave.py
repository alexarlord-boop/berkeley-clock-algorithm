import threading
import time
import socket

from challenges.logging import SynchronizedPrinter
from codes import SlaveCodes, MasterCodes


class SlaveNode(SynchronizedPrinter):
    def __init__(self, port, master_port, time_bias, tag):
        super().__init__()
        self.port = port
        self.master_port = master_port
        self.time_bias = time_bias
        self.tag = tag
        self.running = True  # Flag to control the slave thread

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))

        # 3.1 Connects to master node
        while self.running:
            try:
                server_socket.connect(('localhost', self.master_port))
                self.print_message(f"{self.tag} Connected to master from {self.port}")
                break  # Break out of the loop if connection is successful
            except Exception as e:
                self.print_message(f"{self.tag} Connection to master failed. Retrying... {e}")
                time.sleep(1)

        # 3.2 Disconnects from master node
        if not self.running:
            # 3.4 Termination code
            server_socket.send(SlaveCodes.DEAD.to_bytes())
            server_socket.close()

        # 3.3 Receives time updates, request codes
        try:
            while self.running:
                data = server_socket.recv(1024)

                if data == MasterCodes.REQ_TIME.to_bytes():
                    current_time = time.time()
                    server_socket.send(str(current_time + self.time_bias).encode())

                elif data == MasterCodes.ADJ_TIME.to_bytes():
                    adjusted_time = float(server_socket.recv(1024).decode())
                    self.print_message(f"{self.tag} {self.port} adjust: {adjusted_time}")

                elif data == MasterCodes.REQ_STATUS.to_bytes():
                    server_socket.send(SlaveCodes.ALIVE.to_bytes())

        except Exception as e:
            self.print_message(f"{self.tag} {self.port} thread error: {e}")

    def stop(self):
        # Stop the slave thread
        self.running = False
