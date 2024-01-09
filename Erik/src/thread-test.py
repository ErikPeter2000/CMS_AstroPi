import threading
import queue

queue = queue.Queue()

def myMethod():
    while True:
        item = queue.get(True)
        print(f"received {item}")

thread = threading.Thread(target=myMethod)
thread.start()
while True:
    item = input("Enter something: ")
    queue.put(item)