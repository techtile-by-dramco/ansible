import zmq
import numpy as np
import yaml
import time
from multiprocessing import Process
import argparse
import os

def server(rec_duration, task_port, num_workers):
    context = zmq.Context()

    # PUSH socket 5555 for task distribution
    task_sender = context.socket(zmq.PUSH)
    task_sender.bind("tcp://*:{}".format(task_port))

    # ROUTER socket 5556 for receiving results
    result_receiver = context.socket(zmq.ROUTER)
    result_receiver.bind("tcp://*:{}".format(task_port+1))

    # PUB socket 5557 for sending kill signal
    killer = context.socket(zmq.PUB)
    killer.bind("tcp://*:{}".format(task_port+2))

    print("Wait 10s for all workers connected.")
    time.sleep(10)
    print("Sending tasks to workers.")
    # send tasks
    for task_id in range(num_workers):
        task_cmd = 1
        task = {"task_id": task_id, "task_cmd": task_cmd, "duration": rec_duration}
        task_sender.send_json(task)
    print("All tasks have been sent.")

    # Collecting results from all workers, expect same numeber of results as tasks
    for _ in range(num_workers):
        identity, _, result = result_receiver.recv_multipart()
        if len(result):
            result_conv = np.frombuffer(result, dtype=np.complex64)
            print(f"Received result from {identity.decode()}.")
            if not os.path.exists("data"):
                os.makedirs("data", exist_ok=True)
            np.save('data/' + identity.decode(), result_conv)
        else:
            print(f"Result be processed on board {identity.decode()}.")
    
    print("Sending kill signal.")
    killer.send_string("KILL")

    task_sender.close()
    result_receiver.close()
    killer.close()
    context.term()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', type=str, default=None)
    args = parser.parse_args()
    if args.conf is None:                                     
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
    else:
        with open(args.conf, "r") as f:
            config = yaml.safe_load(f)
    servers = config['servers']
    duration = 5.0
    num_servers = len(servers)
    Processes = []

    for n in range(num_servers):
        Processes.append(Process(target=server, args=(duration, servers[n]['port'], int(servers[n]['connections']), )))
        
    for n in range(len(Processes)):
        Processes[n].start()
    
    for n in range(len(Processes)):
        Processes[n].join()

    print("All tasks are done!")

