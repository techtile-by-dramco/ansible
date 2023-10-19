#!/usr/bin/env /usr/bin/python3

import usrp_receiver as ur

duration = 5.0
channels = 0
rate = 250e3
freq = 900e6
gain = 50

results = ur.rec_samps(duration, channels, rate, freq, gain)
print(results)
