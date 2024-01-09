
#!/usr/bin/env python3
#
# Copyright 2017-2018 Ettus Research, a National Instruments Company
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
Generate and TX samples using a set of waveforms, and waveform characteristics
"""

import time
import argparse
import numpy as np
import uhd
from tone_gen import ToneGenerator
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
    parser.add_argument("-d", "--duration", default=5.0, type=float)
    parser.add_argument("-c", "--channels", default=0, nargs="+", type=int)
    parser.add_argument("-g", "--gain", type=int, default=10)
    parser.add_argument("--wave-freq", default=1e4, type=float)
    parser.add_argument("--wave-ampl", default=0.3, type=float)
    return parser.parse_args()



def multi_usrp_tx(args):
    _rate = float(5e6)
    _amplitude = float(1/np.sqrt(2))
    _tone_freq = 0
    stream_args = uhd.usrp.StreamArgs('fc32', 'sc16')
    channels = args.channels
    _usrp = uhd.usrp.MultiUSRP(args.args)
    for chan in channels:
        _usrp.set_tx_rate(_rate, chan)
        _usrp.set_tx_gain(args.gain, chan)
        _usrp.set_tx_freq(args.f, chan)

    stream_args.channels = args.channels
    
    _streamer = _usrp.get_tx_stream(stream_args)
    
    tone_gen = ToneGenerator(_rate, _tone_freq, _amplitude)
    tone_gen.set_streamer(_streamer)
    tone_gen.start()

def main():
    """TX samples based on input arguments"""
    args = parse_args()
    if not isinstance(args.channels, list):
        args.channels = [args.channels]
    multi_usrp_tx(args)


if __name__ == "__main__":
    main()
