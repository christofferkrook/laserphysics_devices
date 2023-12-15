# load osa_retriever and try the module 

import osa_retriever as osa
import time

# create ando object 
ando = osa.Ando(5)
ando1 = osa.Ando(5)

def fasttask():
    print("Fast task")

# run fasttask continously and also run retrieve_traces from osa_retriever
ando.start()
while True:
    time.sleep(0.1)
    fasttask()

    if ando.trace_queue.empty():
        continue
    else:
        print("It is not empty")
        traces = ando.trace_queue.get()
        print("Got traces from queue")

    