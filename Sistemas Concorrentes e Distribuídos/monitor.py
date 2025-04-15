import threading
import time
import random
from collections import deque

class BufferMonitor:
    def __init__(self, size):
        self.buffer = deque()
        self.size = size
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def put(self, item, pid):
        with self.lock:
            while len(self.buffer) == self.size:
                print(f"[{time.strftime('%H:%M:%S')}] Produtor {pid} aguardando (buffer cheio)")
                self.not_full.wait()

            self.buffer.append(item)
            print(f"[{time.strftime('%H:%M:%S')}] Produtor {pid} produziu {item}. Buffer agora: {list(self.buffer)}")

            time.sleep(2)
            self.not_empty.notify()

    def get(self, cid):
        with self.lock:
            while len(self.buffer) == 0:
                print(f"[{time.strftime('%H:%M:%S')}] Consumidor {cid} aguardando (buffer vazio)")
                self.not_empty.wait()

            item = self.buffer.popleft()
            print(f"[{time.strftime('%H:%M:%S')}] Consumidor {cid} consumiu {item}. Buffer agora: {list(self.buffer)}")

            time.sleep(2)
            self.not_full.notify()

monitor = BufferMonitor(size=3)

def producer(pid):
    time.sleep(random.uniform(2.0, 4.0))
    item = random.randint(1, 100)
    print(f"[{time.strftime('%H:%M:%S')}] Produtor {pid} tentando produzir {item}")
    monitor.put(item, pid)

def consumer(cid):
    time.sleep(random.uniform(2.0, 4.0))
    print(f"[{time.strftime('%H:%M:%S')}] Consumidor {cid} tentando consumir")
    monitor.get(cid)

threads = []
for i in range(6):
    if i % 2 == 0:
        t = threading.Thread(target=producer, args=(i,))
    else:
        t = threading.Thread(target=consumer, args=(i,))
    threads.append(t)
    t.start()
    time.sleep(1)

for t in threads:
    t.join()

print("Fim da execução.")
