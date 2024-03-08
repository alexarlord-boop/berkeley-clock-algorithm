import threading
import time

from challenges.node_management import simulate_slave_lifecycle
from master import MasterNode
from utilities.ports import find_free_ports
from settings import general_latency, separator, master_tag, start_tag, simulation_duration

if __name__ == "__main__":
    free_ports = find_free_ports(5000, 6000, 1)
    master_port = free_ports[0]
    master = MasterNode(port=master_port, tag=master_tag)

    # start the master thread
    master_thread = threading.Thread(target=master.run)
    master_thread.start()

    # give it some extra time for the server to set up
    time.sleep(2)
    print(f"{start_tag} Master thread for port {master_port} started.")

    # start simulating dynamic slave lifecycle
    simulate_thread = threading.Thread(target=simulate_slave_lifecycle, args=(master, simulation_duration))
    simulate_thread.start()

    while True:
        master.synchronize_clocks()
        time.sleep(general_latency)
        print(separator + f"{general_latency} seconds of M-S communication passed" + separator)
