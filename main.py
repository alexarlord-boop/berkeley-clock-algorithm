# Inside main.py
import threading
import time
from master import MasterNode
from ports import find_free_ports
from slave import SlaveNode

if __name__ == "__main__":
    general_latency = 5
    slave_n = 4
    separator = "-" * 10
    free_ports = find_free_ports(5000, 6000, slave_n + 1)
    master_port = free_ports[0]
    slave_ports = free_ports[1::]

    master = MasterNode(port=master_port)
    slaves = [SlaveNode(port=port, master_port=master_port) for port in slave_ports]

    # Start the master thread
    master_thread = threading.Thread(target=master.run)
    master_thread.start()

    # Give it some extra time for the server to set up
    time.sleep(2)
    print(f"Master thread is running on {master_port}.")

    for slave in slaves:
        threading.Thread(target=slave.run).start()
        print(f"Slave thread for port {slave.port} started.")

    while True:
        master.synchronize_clocks()
        time.sleep(general_latency)
        print(separator + f"{general_latency} seconds passed" + separator)
