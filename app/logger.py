import time

class Logger:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def end(self, label: str):
        if self.start_time:
            print(f"[{label}] Time: {time.time() - self.start_time:.2f}s")