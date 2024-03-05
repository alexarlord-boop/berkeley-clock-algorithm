
class Node:
    def __init__(self, node_type, port, tag, time_bias, master_port):
        self.node_type = node_type
        self.port = port
        self.master_port = master_port  # equals to port if master
        self.time_bias = time_bias  # equals to 0 if master
        self.tag = tag
        self.running = True

    def run(self): pass
    def stop(self): pass
