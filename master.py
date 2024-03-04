# Inside MasterNode class in master.py
import threading
import time
import socket
from random import random

from challenges.logging import SynchronizedPrinter
from settings import slave_n
from codes import SlaveCodes, MasterCodes


class MasterNode(SynchronizedPrinter):
    def __init__(self, port, tag):
        super().__init__()
        self.port = port
        self.slaves = {}  # {'port': [(conn, addr), time]}
        self.lock = threading.Lock()
        self.tag = tag

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
            # Handle master failure, initiate reelection
            self.initiate_master_reelection()
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

    def initiate_master_reelection(self):
        with self.lock:
            # Simple reelection logic: select a random slave as the new master
            if self.slaves:
                new_master_port = random.choice(list(self.slaves.keys()))
                new_master_addr = self.slaves[new_master_port][0][1]
                self.print_message(f"{self.tag} Initiating master reelection. New master: {new_master_addr}")
                # You may want to notify other slaves about the new master
