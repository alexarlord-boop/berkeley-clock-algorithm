import threading
import time

from challenges.logging import SynchronizedPrinter
from master import MasterNode

# all nodes can be a master node
# nodes generated, one of them is chosen as master
# master works, then die
# new master elected from rest nodes

# in my first approach I strictly divided master and slave functionality, and it is not suitable for this challenge.
# apparently, all nodes should have master and slave methods, choice of which is based on the node mode.
# For implementing this task I will create a new branch for experiments

# def simulate_master_lifecycle(master, duration):
#     sync_printer = SynchronizedPrinter()
#     time.sleep(2)  # Give some time for initial setup
#     start_time = time.time()
#
#     while time.time() - start_time < duration:
#         # Simulate master node stopping and restarting
#         master.stop()  # Assuming you have a stop method in your MasterNode class
#         sync_printer.print_message(f"Master node stopped.")
#
#         time.sleep(5)  # Adjust the sleep duration based on your needs
#
#         master = MasterNode(port=master.port, tag=master.tag)
#         threading.Thread(target=master.run).start()
#         sync_printer.print_message(f"Master node restarted.")
#
#         time.sleep(10)  # Adjust the sleep duration based on your needs
#
