import uhd
import numpy as np

def check_channels(usrp, channels):
    """Check that the device has sufficient RX channels available"""
    # Check that each channel specified is less than the number of total number of rx channels
    # the device can support
    dev_rx_channels = usrp.get_rx_num_channels()
    if not all(map((lambda chan: chan < dev_rx_channels), channels)):
        print("Invalid channel(s) specified.")
        return []
    return channels

def rec_samps(duration, channels, rate, freq, gain):
    """RX samples and write to file"""
    usrp = uhd.usrp.MultiUSRP("")
    # Set the channel
    if not isinstance(channels, list):
        channels = [channels]
    chan = channels[0]
    
    #Set the rate 
    usrp.set_rx_rate(rate, chan)
    actual_rate = usrp.get_rx_rate(chan)
    print(f"Requesting sampling rate {rate/1e6} Msps...")
    print(f"Using sampling rate: {actual_rate/1e6} Msps.")

    # Set the frequecy
    usrp.set_rx_freq(freq, chan)
    print(f"Requesting center frequency {freq/1e6} MHz...")
    print(f"Actual center frequency: {usrp.get_rx_freq(chan)/1e6} MHz.")

    #Set the gain
    usrp.set_rx_gain(gain, chan)
    print(f"Requesting gain {gain} dB...")
    print(f"Actual gain: {usrp.get_rx_gain(chan)} dB.")

    channels = check_channels(usrp, channels)
    if not channels:
        return False
    else:
        print("channel checked")
    
    stream_args = uhd.usrp.StreamArgs("fc32", "sc16")
    stream_channels = channels
    rx_streamer = usrp.get_rx_stream(stream_args)

    num_channels = rx_streamer.get_num_channels()
    metadata = uhd.types.RXMetadata()
    if num_channels == 1:
        print("Starting stream...")

        buffer_samps = rx_streamer.get_max_num_samps()
        print(f"max num samps: {buffer_samps}")
        
        recv_buffer = np.zeros((len(channels), buffer_samps), dtype=np.complex64)        
        recv_samps = 0
        samps = np.array([], dtype=np.complex64)
        num_samps = int(np.ceil(duration*rate))
        print(f"expected num samps: {num_samps}")
        result = np.empty((len(channels), num_samps), dtype=np.complex64)

        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.num_done)
        stream_cmd.num_samps = int(rate * duration)
        stream_cmd.stream_now = True
        
        rx_streamer.issue_stream_cmd(stream_cmd)
        while recv_samps < num_samps:
            samps = rx_streamer.recv(recv_buffer, metadata)

            if metadata.error_code != uhd.types.RXMetadataErrorCode.none:
                print(metadata.strerror())
                break
            if samps:
                real_samps = min(num_samps - recv_samps, samps)
                result[:, recv_samps:recv_samps + real_samps] = recv_buffer[:, 0:real_samps]
                recv_samps += real_samps

        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
        rx_streamer.issue_stream_cmd(stream_cmd)
        print("Stop straming.")

        # Garbage collection
        while samps:
            samps = rx_streamer.recv(recv_buffer, metadata)
        rx_streamer = None
        return result
