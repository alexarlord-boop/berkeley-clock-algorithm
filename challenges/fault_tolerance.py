# all nodes can be a master node
# nodes generated, one of them is chosen as master
# master works, then die
# new master elected from rest nodes
import random
import threading
import time

from Node import Node
from utilities.ports import find_free_ports
from utilities.logging import SynchronizedPrinter



# in my first approach I strictly divided master and slave functionality, and it is not suitable for this challenge.
# apparently, all nodes should have master and slave methods, choice of which is based on the node mode.

class DistributedSystem(SynchronizedPrinter):
    def __init__(self):
        super().__init__()
        self.ports = []
        self.nodes = []

    def update_ports(self):
        # finds free ports
        pass

    def update_nodes(self):
        # allocate new nodes to existing ports
        pass

    def choose_master(self):
        master_node = random.choice(self.nodes)
        master_node.is_master = True
        self.print_message("new master selected")

    def kill_node(self, node):
        node.stop()
        self.nodes.remove(node)

    def init_network(self):
        # starts threads for master, then slave nodes
        threads = [threading.Thread(target=node.run) for node in self.nodes]
        for thread in threads:
            thread.start()


if __name__ == "__main__":
    distributed_system = DistributedSystem()
    free_ports = find_free_ports(5000, 6000, 5)  # Assuming 5 nodes
    for i, port in enumerate(free_ports):
        node = Node(port=port, tag=f"Node-{i}", time_bias=random.randint(1, 10))
        distributed_system.nodes.append(node)

    distributed_system.choose_master()
    distributed_system.init_network()

    try:
        while True:
            time.sleep(5)
            for node in distributed_system.nodes:
                pass
                # node.print_message(f"{node.tag} hi")
    except KeyboardInterrupt:
        for node in distributed_system.nodes:
            node.stop()
