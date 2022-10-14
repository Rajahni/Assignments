import threading
from threading import Condition

condition = Condition()

def producer(message,queue,capacity):
    global messagelen
    condition.acquire()
    print("Producer started")
    ## Loops through the message and adds each character to the queue
    for char in message:
        # Checks to see if the queue is full and if it is it waits for the consumer to empty it
        if len(queue) == capacity:
            print(len(queue))
            print(capacity)
            print("Queue full, producer is waiting")
            print(queue)
            condition.wait()
        queue.append(char)
        print(queue)
        # Shortens message amount left to go through 
        message = message[1:] 
        messagelen = len(message)
        print ("left",message)
        condition.notify()
    condition.release()
    print("Producer finished")

def capitalizer(queue,message):
    condition.acquire() 
    print("Capitalizer started")
    if len(queue) != 0:
        # Loops through the queue and capitalizes each character
        for i in range(len(queue)):
            queue[i] = queue[i].upper()
        print(queue)
        print(len(message))
        if messagelen != 0:
            print("0",messagelen)
            condition.wait()
    if messagelen == 0:
        for i in range(len(queue)):
            queue[i] = queue[i].upper()
        print(queue)
        print("=0,",messagelen)
        condition.notify()
   # if len(queue) == 0:
    #    print("Queue empty, capitalizer is waiting")
     #   condition.wait()
    condition.release()
    print("Capitalizer finished")

def consumer(queue,message):
    condition.acquire()
    print("Consumer started")
    print("a",queue)
    if len(queue) != 0:
        print(len(queue))
        for i in range(len(queue)):
            print(i)
            for j in range(5):
                x = queue.pop()
                print(x,queue)
    if messagelen != 0:
        print("b")
        condition.notify()
        condition.wait()
    
    print(len(queue))
    condition.release()
    print("Consumer finished")


queue = []
capacity = 12
message = ""

print("Enter a message under 255 characters: ")
message = input()


producer = threading.Thread(target=producer,args=(message,queue,capacity))
capitalizer = threading.Thread(target=capitalizer,args=(queue,message))
consumer = threading.Thread(target=consumer,args=(queue,message))

producer.start()
capitalizer.start()
consumer.start()


producer.join()
capitalizer.join()
consumer.join()