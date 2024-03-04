# Inside main.py
import threading
import time

from challenges.node_management import simulate_slave_lifecycle
from master import MasterNode
from ports import find_free_ports
from settings import general_latency, separator, master_tag, start_tag
from slave import SlaveNode

if __name__ == "__main__":
    free_ports = find_free_ports(5000, 6000, 1)
    master_port = free_ports[0]
    # slave_ports = free_ports[1::]

    master = MasterNode(port=master_port, tag=master_tag)
    # slaves = [SlaveNode(port=port, master_port=master_port, tag=slave_tag) for port in slave_ports]

    # Start the master thread
    master_thread = threading.Thread(target=master.run)
    master_thread.start()

    # Give it some extra time for the server to set up
    time.sleep(2)
    print(f"{start_tag} Master thread for port {master_port} started.")

    # Start simulating dynamic slave lifecycle
    simulate_thread = threading.Thread(target=simulate_slave_lifecycle, args=(master, 60))
    simulate_thread.start()

    while True:
        master.synchronize_clocks()
        time.sleep(general_latency)
        print(separator + f"{general_latency} seconds of M-S communication passed" + separator)
