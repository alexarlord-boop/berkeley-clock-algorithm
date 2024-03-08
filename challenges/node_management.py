import threading
import time

from utilities.logging import SynchronizedPrinter
from utilities.ports import find_free_ports
from settings import slave_tag, start_tag, stop_tag, slave_n, slave_lifetime
from slave import SlaveNode
import random


def get_time_bias(i):
    k = 2 * i
    # Randomize the bias based on the factor k
    random_bias = random.uniform(-k, k)
    return random_bias


def simulate_slave_lifecycle(master, duration):
    sync_printer = SynchronizedPrinter()
    time.sleep(2)  # Give some time for initial setup
    start_time = time.time()

    while time.time() - start_time < duration:

        # Simulate slaves joining dynamically
        new_slave_ports = find_free_ports(6000, 7000, slave_n)
        new_slaves = [SlaveNode(port=p,
                                master_port=master.port,
                                time_bias=get_time_bias(new_slave_ports.index(p) + 1),
                                tag=slave_tag)
                      for p in new_slave_ports]

        for slave in new_slaves:
            threading.Thread(target=slave.run).start()
        slaves = new_slaves

        sync_printer.print_message(f"{start_tag} New slave threads for ports {new_slave_ports} started.")

        time.sleep(slave_lifetime)  # Adjust the sleep duration based on your needs

        # Simulate slaves leaving dynamically
        if slaves:
            leaving_slave = slaves.pop(0)
            leaving_slave.stop()  # Assuming you have a stop method in your SlaveNode class
            sync_printer.print_message(f"{stop_tag} Slave thread for port {leaving_slave.port} stopped.")
