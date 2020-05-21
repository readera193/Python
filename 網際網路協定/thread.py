
import threading
import time


class Bg(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        for i in range(10, 0, -1):
            print(i)
            time.sleep(1)
        print(0)

t1 = Bg()
#t1.daemon = True
t1.start()

print("Count down from 10.")
time.sleep(3)
print("7 seconds")
time.sleep(4)
print("3 seconds")
t1.join()     # Try to comment this line.
print('finish')
