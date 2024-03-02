# Inside SlaveNode class in slave.py
import threading
import time
import socket


class SlaveNode:
    def __init__(self, port, master_port):
        self.port = port
        self.master_port = master_port

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        connected = False
        while not connected:
            try:
                server_socket.connect(('localhost', self.master_port))
                connected = True
            except Exception as e:
                print(f"Connection to master failed. Retrying... {e}")
                time.sleep(1)

        try:
            while True:
                data = server_socket.recv(1024)
                if data == b"REQUEST_TIME":
                    current_time = time.time()
                    server_socket.send(str(current_time).encode())
                elif data == b"ADJUST_TIME":
                    adjusted_time = float(server_socket.recv(1024).decode())
                    print(f"\tSlave {self.port} Adjusted Time: {adjusted_time}")
                else:
                    # Handle other cases if needed
                    pass
        except Exception as e:
            print(f"Slave {self.port} thread error: {e}")
        finally:
            server_socket.close()
