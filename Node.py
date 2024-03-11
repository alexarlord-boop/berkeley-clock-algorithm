import settings


class Node:
    def __init__(self, port, tag, time_bias):
        self.port = port
        self.time_bias = time_bias  # equals to 0 if master
        self.tag = tag
        self.is_master = False
        self.is_alive = True
        self.time_to_live = 10

    def run(self): pass
    def stop(self): pass
