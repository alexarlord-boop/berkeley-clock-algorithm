from master import MasterNode
from slave import SlaveNode


def start_master(port):
    master = MasterNode(port)
    master.start()


def start_slave(slave_port, master_port):
    slave = SlaveNode(slave_port, master_port)
    slave.connect_to_master()
    slave.start()
