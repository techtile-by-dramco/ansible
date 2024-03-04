import argparse
import pll
import time 

# Initialize the parser
parser = argparse.ArgumentParser(description='PLL')
parser.add_argument('arg1', type=int)

# Define arguments
args = parser.parse_args()

# Access the arguments
freq = args.arg1


p = pll.PLL()
#p.power(1)
p.set_LED_mode(pll.LED_MODE_LOCK_DETECT)
time.sleep(0.1)
#p.set_PLL_reference_clock(10.0)
time.sleep(0.1)
#print(p.get_PLL_reference_clock())
time.sleep(0.1)
#print(p.get_PLL_reference_divider())
time.sleep(0.1)
p.power_on()
p.enable_output()
p.frequency(freq)
while not p.locked():
	print("Not locked")
	time.sleep(0.5)
