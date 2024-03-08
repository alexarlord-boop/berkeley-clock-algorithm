import threading


class SynchronizedPrinter:
    def __init__(self):
        self.print_lock = threading.Lock()

    def print_message(self, message):
        with self.print_lock:
            print(message)
