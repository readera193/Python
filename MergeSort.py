import multiprocessing
import logging

def main():
    import sys
    from random import randint
    if len(sys.argv) == 2:
        N = int(sys.argv[1])
    else:
        N = 8
    aList = [randint(1, N*N) for i in range(N)]
    print(aList)
    a, b = multiprocessing.Pipe()
    p = multiprocessing.Process(target=mergeSort, args=(b,))
    a.send((aList, 0, N))
    p.start()
    p.join()
    bList = a.recv()
    print(bList)
    
def mergeSort(connect):
    array, left, right = connect.recv()
    connect.send((array, left, right))
    if left >= right:
        connect.send(array)
        return
    
    import math
    mid = math.floor( (left+right)/2 )
    a, b = multiprocessing.Pipe()
    procLeft = multiprocessing.Process(target=mergeSort, args=(b,))
    a.send((array, left, mid))
    procLeft.start()
    arrayLeft = a.recv()
    
    c, d = multiprocessing.Pipe()
    procRight = multiprocessing.Process(target=mergeSort, args=(d,))
    c.send((array, mid, right))
    procRight.start()
    arrayRight = c.recv()
    
    procLeft.join()
    procRight.join()
    
    return merge(arrayLeft, arrayRight)
    
def merge(arrayLeft, arrayRight):
    result = []
    i=j=0
    while (i<len(arrayLeft) and j<len(arrayRight)):
        if arrayLeft[i] <= arrayRight[j]:
            result.append(arrayLeft[i])
            i+=1
        else:
            result.append(arrayRight[j])
            j+=1
    while i<len(arrayLeft):
        result.append(arrayLeft[i])
        i+=1
    while j<len(arrayRight):
        result.append(arrayRight[j])
        j+=1
    return result
    
if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] (%(threadName)-10s) %(message)s',)
    main()