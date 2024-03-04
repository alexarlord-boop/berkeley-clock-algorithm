import socket


def find_free_ports(start_port, end_port, num_ports):
    free_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout for the connection attempt

        try:
            sock.bind(('localhost', port))
            free_ports.append(port)
        except OSError:
            pass  # Port is not available

        sock.close()

        if len(free_ports) == num_ports:
            break
    # print("Free ports:", free_ports)
    return free_ports

# # Example usage: find 2 free ports between 5000 and 6000
# free_ports = find_free_ports(5000, 6000, 4)
# print("Free ports:", free_ports)
