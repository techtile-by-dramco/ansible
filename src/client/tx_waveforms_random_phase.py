"""
0. start server "random_phases_ZMQ"
1. wait till random phase (step 2) or STOP (step 4) command of server
2. change phase randomnly and transmit for 'duration' seconds at next PPS
3. go to step 1.
4. stop

--ip "IP OF ZMQ SERVER"

Server port: 5558 topic: phase commands: start or stop


"""

import time
import argparse
import numpy as np
import uhd
#from uhd.usrp import dram_utils


def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--args", default="", type=str)
    parser.add_argument(
        "-w", "--waveform", default="sine",
        choices=['sine', 'square', 'const', 'ramp'], type=str)
    parser.add_argument("-f", "--freq", type=float, required=True)
    parser.add_argument("-r", "--rate", default=1e6, type=float)
    parser.add_argument("-d", "--duration", default=1.0, type=float)
    parser.add_argument("-c", "--channels", default=0, nargs="+", type=int)
    parser.add_argument("-g", "--gain", type=float, default=10.0)
    parser.add_argument("--wave-freq", default=1e4, type=float)
    parser.add_argument("--wave-ampl", default=0.3, type=float)
    parser.add_argument("--ip", required=True, type=str)
    return parser.parse_args()

import zmq

def wait_till_go_from_server(ip:str):
    """Wait till a message is received at ip:5557 for topic phase.

    Args:
        ip (str): IP Address of the server
    """
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    socket.connect(f"tcp://{ip}:{5558}")  # Connect to the publisher's address

    # Subscribe to topics
    socket.subscribe("phase")
    # Receives a string format message
    cmd = socket.recv_string()
    print(cmd)

    return cmd.lower()=="start"

def config_streamer(args, usrp):
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    st_args.channels = args.channels
    return usrp.get_tx_stream(st_args)

def send_waveform(usrp, waveform_proto,
                      duration,
                      freq,
                      streamer,
                      rate=1e6,
                      channels=(0,),
                      gain=10,
                      start_time=None):
    """
    TX a finite number of samples from the USRP
    :param waveform_proto: numpy array of samples to TX
    :param duration: time in seconds sending at constant random phase
    :param freq: TX frequency (Hz)
    :param rate: TX sample rate (Hz)
    :param channels: list of channels to TX on
    :param gain: TX gain (dB)
    :param start_time: A valid TimeSpec object with the starting time. If
                        None, then streaming starts immediately.
    :param streamer: A TX streamer object. If None, this function will create
                        one locally and attempt to destroy it afterwards.
    :return: the number of transmitted samples
    """
    
    ## And go!
    for chan in channels:
        usrp.set_tx_rate(rate, chan)
        usrp.set_tx_freq(uhd.types.TuneRequest(freq), chan)
        usrp.set_tx_gain(gain, chan)

    # Set up buffers and counters
    buffer_samps = streamer.get_max_num_samps()
    proto_len = waveform_proto.shape[-1]
    if proto_len < buffer_samps:
        waveform_proto = np.tile(waveform_proto,
                                    (1, int(np.ceil(float(buffer_samps)/proto_len))))
        proto_len = waveform_proto.shape[-1]
    send_samps = 0
    max_samps = int(np.floor(duration * rate))
    if len(waveform_proto.shape) == 1:
        waveform_proto = waveform_proto.reshape(1, waveform_proto.size)
    if waveform_proto.shape[0] < len(channels):
        waveform_proto = np.tile(waveform_proto[0], (len(channels), 1))
    # multiply waveform_proto with fixed random phase per channel
    waveform_proto *=  np.exp(1j*np.random.rand((len(channels), 1))*2*np.pi)
    # Now stream
    metadata = uhd.types.TXMetadata()
    if start_time is not None:
        metadata.time_spec = start_time
        metadata.has_time_spec = True
    while send_samps < max_samps:
        real_samps = min(proto_len, max_samps-send_samps)
        if real_samps < proto_len:
            samples = streamer.send(waveform_proto[:, :real_samps], metadata)
        else:
            samples = streamer.send(waveform_proto, metadata)
        send_samps += samples
    # Send EOB to terminate Tx
    metadata.end_of_burst = True
    streamer.send(np.zeros((len(channels), 1), dtype=np.complex64), metadata)
    # Help the garbage collection
    streamer = None
    return send_samps

def multi_usrp_tx(args):
    """
    multi_usrp based TX example
    """
    usrp = uhd.usrp.MultiUSRP(args.args)
    usrp.set_clock_source("external")
    usrp.set_time_source("external")
    tx_streamer = config_streamer(args, usrp)
    if args.wave_freq == 0.0:
        desired_size = 1e6 # Just pick a value
    else:
        desired_size = 10 * np.floor(args.rate / args.wave_freq)
    data = uhd.dsp.signals.get_continuous_tone(
        args.rate,
        args.wave_freq,
        args.wave_ampl,
        desired_size=desired_size,
        max_size=(args.duration * args.rate))
    
    start = wait_till_go_from_server(args.ip)
    while(start):
        send_waveform(data, args.duration, args.freq, args.rate,
                        args.channels, args.gain, tx_streamer)
        start = wait_till_go_from_server(args.ip)

def main():
    """TX samples based on input arguments"""
    args = parse_args()
    if not isinstance(args.channels, list):
        args.channels = [args.channels]
    multi_usrp_tx(args)

if __name__ == "__main__":
    main()
