# Inside MasterNode class in master.py
import threading
import time
import socket


class MasterNode:
    def __init__(self, port):
        self.port = port
        self.slaves = []
        self.clock_offset = 0
        self.lock = threading.Lock()

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind(('localhost', self.port))
            server_socket.listen(5)

            while True:
                conn, addr = server_socket.accept()
                threading.Thread(target=self.handle_slave, args=(conn, addr)).start()
        except Exception as e:
            print(f"Master thread error: {e}")
        finally:
            server_socket.close()

    def handle_slave(self, conn, addr):
        with self.lock:
            self.slaves.append((conn, addr))
            print(f"Slave connected from {addr}")

    def synchronize_clocks(self):
        with self.lock:
            if len(self.slaves) > 0:
                current_times = [time.time()]  # we add master node current time
                for conn, addr in self.slaves:
                    try:
                        conn.send(b"REQUEST_TIME")
                        data = conn.recv(1024)
                        current_time = float(data.decode())
                        current_times.append(current_time)  # and then add slave nodes current time
                    except Exception as e:
                        print(f"Error communicating with slave {addr}: {e}")

                if current_times:
                    print(current_times)
                    average_time = sum(current_times) / len(current_times)
                    self.clock_offset = time.time() - average_time

                    for conn, addr in self.slaves:
                        adjusted_time = time.time() - self.clock_offset
                        try:
                            conn.send(b"ADJUST_TIME")
                            conn.send(str(adjusted_time).encode())
                        except Exception as e:
                            print(f"Error communicating with slave {addr}: {e}")
