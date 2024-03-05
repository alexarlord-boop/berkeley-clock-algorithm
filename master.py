# Inside MasterNode class in master.py
import threading
import time
import socket
from random import random

from Node import Node
from challenges.logging import SynchronizedPrinter
from settings import slave_n
from codes import SlaveCodes, MasterCodes, NodeType


class MasterNode(SynchronizedPrinter, Node):
    def __init__(self, port, tag):
        super().__init__()
        self.node_type = NodeType.MASTER.to_bytes()
        self.port = port
        self.master_port = port
        self.time_bias = 0
        self.tag = tag
        self.running = True

        # master node specific attributes
        self.lock = threading.Lock()
        self.slaves = {}  # {'port': [(conn, addr), time]}

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind(('localhost', self.port))
            server_socket.listen(slave_n)  # set the number of allowed connections = number of slave nodes

            while True:
                conn, addr = server_socket.accept()
                conn.setblocking(True)  # Set the accepted socket to blocking mode
                threading.Thread(target=self.handle_slave, args=(conn, addr)).start()
        except Exception as e:
            self.print_message(f"{self.tag} thread error: {e}")
        finally:
            server_socket.close()

    def handle_slave(self, conn, addr):
        with self.lock:
            port = addr[1]
            if port not in self.slaves:
                self.slaves[port] = [(conn, addr), 0]
                self.print_message(f"{self.tag} Slave connected from {addr}")
                # threading.Thread(target=self.monitor_slave, args=(port,)).start()

    def synchronize_clocks(self):
        keys_to_remove = []

        # checking if slave nodes are alive and request times
        for port, [conn_info, _] in self.slaves.items():
            conn, addr = conn_info

            try:
                conn.send(MasterCodes.REQ_STATUS.to_bytes())
                data = conn.recv(1024)
                if data == SlaveCodes.DEAD.to_bytes():
                    keys_to_remove.append(port)
            except Exception as e:
                self.print_message(f"{self.tag} Error communicating with slave {addr}: {e}")
                keys_to_remove.append(port)

        # remove invalid nodes
        for port in keys_to_remove:
            del self.slaves[port]  # Remove the slave entry from the dictionary

        # process alive nodes
        with self.lock:
            if self.slaves:
                master_time = time.time()
                current_times = [master_time]  # we add master node current time
                for port, [conn_info, slave_old_time] in self.slaves.items():
                    conn, addr = conn_info
                    try:
                        conn.send(MasterCodes.REQ_TIME.to_bytes())
                        data = conn.recv(1024)
                        current_time = float(data.decode())
                        self.slaves[port][1] = current_time  # update tmp time value for the slave
                        current_times.append(current_time)  # and then add slave node time for further calcs
                    except Exception as e:
                        self.print_message(f"{self.tag} Error communicating with slave {addr}: {e}")

                # calc new time for the live slave nodes
                if current_times:
                    self.print_message(f"{self.tag} timestamps: {current_times}")

                    for port, [conn_info, slave_old_time] in self.slaves.items():
                        conn, addr = conn_info
                        slave_offset = master_time - slave_old_time
                        adjusted_time = slave_old_time + slave_offset
                        try:
                            conn.send(MasterCodes.ADJ_TIME.to_bytes())
                            conn.send(str(adjusted_time).encode())
                            self.print_message(f"{self.tag} {port} offset: {slave_offset}")
                        except Exception as e:
                            self.print_message(f"{self.tag} Error communicating with slave {addr}: {e}")

