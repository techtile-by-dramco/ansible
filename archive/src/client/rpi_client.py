import zmq
import socket
import usrp_receiver as ur
import numpy as np
import argparse

def worker(port, channels, freq, rate, gain):
    context = zmq.Context()

    # PULL socket for receiving tasks
    task_receiver = context.socket(zmq.PULL)
    task_receiver.connect("tcp://192.108.0.1:{}".format(port))

    # DEALER socket for sending results
    result_sender = context.socket(zmq.DEALER)
    result_sender.setsockopt_string(zmq.IDENTITY, socket.gethostname()) 
    result_sender.connect("tcp://192.108.0.1:{}".format(port+1))

    #SUB socket for receiving killing signals
    killer = context.socket(zmq.SUB)
    killer.connect("tcp://192.108.0.1:{}".format(port+2))
    killer.setsockopt_string(zmq.SUBSCRIBE, "")

    poller = zmq.Poller()
    poller.register(task_receiver, zmq.POLLIN)
    poller.register(killer, zmq.POLLIN)

    while True:
        socks = dict(poller.poll())
        if socks.get(task_receiver) == zmq.POLLIN:
            task = task_receiver.recv_json(flags=zmq.NOBLOCK)
            task_id = task["task_id"]
            task_cmd = task["task_cmd"]
            duration = task["duration"]
            print(f"Received task with ID: {task_id}")

            # Perform tasks
            channels = 0
            rate = 250e3
            freq = 900e6
            gain = 50
            results = ur.rec_samps(duration, channels, rate, freq, gain)
            if task_cmd:                
                result_sender.send_multipart([b'', results.tobytes()])
                print('Sent results.')
            else:
                np.save(socket.gethostname(), results)
                result_sender.send_multipart([b'', b''])
                print('Stored results.')
            
        if socks.get(killer) == zmq.POLLIN:
            signal = killer.recv_string()
            if signal == 'KILL':
                print('Received kill signal, exit.')
                break
                
    task_receiver.close()
    result_sender.close()
    killer.close()
    context.term()

def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=5555, type=int)
    parser.add_argument("-c", "--channels", default=0, type=int)
    parser.add_argument("-f", "--freq", default=900e6, type=float)
    parser.add_argument("-r", "--rate", default=250e3, type=float)
    parser.add_argument("-g", "--gain", default=50, type=int)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    worker(args.port, args.channels, args.freq, args.rate, args.gain)
