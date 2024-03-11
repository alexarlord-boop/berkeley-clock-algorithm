# all nodes can be a master node
# nodes generated, one of them is chosen as master
# master works, then die
# new master elected from rest nodes

# in my first approach I strictly divided master and slave functionality, and it is not suitable for this challenge.
# apparently, all nodes should have master and slave methods, choice of which is based on the node mode.

class DistributedSystem:
    def __init__(self):
        self.ports = []
        self.nodes = []

    def update_ports(self):
        # finds free ports
        pass

    def update_nodes(self):
        # allocate new nodes to existing ports
        pass

    def choose_master(self):
        # randomly sets a node.is_master = True
        pass

    def kill_node(self):
        # disconnects and removes node
        pass

    def init_network(self):
        # starts threads for master, then slave nodes
        pass

