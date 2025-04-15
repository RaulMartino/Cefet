import threading
import time
import random
from collections import deque

BUFFER_SIZE = 5
buffer = deque()

# Semáforos
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)
mutex = threading.Semaphore(1)

log_lock = threading.Lock()
log_counter = {"produzidos": 0, "consumidos": 0}

def log(msg):
    with log_lock:
        print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def producer(pid):
    time.sleep(random.uniform(0.1, 1))
    item = random.randint(1, 100)

    log(f"Produtor {pid} tentando produzir...")

    empty.acquire()
    log(f"Produtor {pid} passou empty.acquire() (espaco disponível)")

    mutex.acquire()
    log(f"Produtor {pid} entrou na seção crítica")

    buffer.append(item)
    log_counter["produzidos"] += 1
    log(f"Produtor {pid} produziu {item}. Buffer: {list(buffer)}")

    mutex.release()
    full.release()
    log(f"Produtor {pid} sinalizou full (item disponível)")

def consumer(cid):
    time.sleep(random.uniform(0.1, 1))

    log(f"Consumidor {cid} tentando consumir...")

    full.acquire()
    log(f"Consumidor {cid} passou full.acquire() (item disponível)")

    mutex.acquire()
    log(f"Consumidor {cid} entrou na seção crítica")

    item = buffer.popleft()
    log_counter["consumidos"] += 1
    log(f"Consumidor {cid} consumiu {item}. Buffer: {list(buffer)}")

    mutex.release()
    empty.release()
    log(f"Consumidor {cid} sinalizou empty (espaço liberado)")

threads = []
for i in range(10):
    if i % 2 == 0:
        t = threading.Thread(target=producer, args=(i,))
    else:
        t = threading.Thread(target=consumer, args=(i,))
    threads.append(t)
    t.start()
    time.sleep(random.uniform(0.05, 0.3))

for t in threads:
    t.join()

log(f"Resumo final: produzidos={log_counter['produzidos']}, consumidos={log_counter['consumidos']}")
log("Fim da execução.")