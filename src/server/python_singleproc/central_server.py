import zmq
import numpy as np
import time
import yaml
import os

def server(rec_duration, task_port, workerCount):
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

    # send heartbeat to all subscribers

    print("Sending tasks to workers.")
    # send tasks
    for task_id in range(workerCount):
        task_cmd = 1
        task = {"task_id": task_id, "task_cmd": task_cmd, "duration": rec_duration}
        task_sender.send_json(task)
    print("All tasks have been sent.")

    # Collecting results from all workers, expect same numeber of results as tasks
    for _ in range(workerCount):
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
    with open("../server_config.yaml", "r") as f:
        config = yaml.safe_load(f)
    duration = 5.0
    port = 5555
    connections = config['servers'][0]['connections']
    server(duration, port, int(connections))
