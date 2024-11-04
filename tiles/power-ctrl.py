# Script to control the PoE power to the hosts. 

#   INFO
server_user_name = "techtile"
inventory=f"/home/{server_user_name}/ansible/inventory/hosts.yaml"

tiles = "G01"
#action = 0  # OFF
action = 0  # ON

# *** Includes ***
import sys

try:
    import importlib
    import importlib.util
    import importlib.machinery

    try:
        PY_MAGIC_NUMBER = importlib.util.MAGIC_NUMBER
        SOURCE_SUFFIXES = importlib.machinery.SOURCE_SUFFIXES
        BYTECODE_SUFFIXES = importlib.machinery.BYTECODE_SUFFIXES

    except Exception:
        raise ImportError()

except ImportError:
    print("Shit just hit the fan.")

sys.path.append("./support")

# make sure to set the secrets!
from support import secrets

from support import midspan_support_class
midspan = midspan_support_class.midspan_support_class(secrets.midspan_login, secrets.midspan_pw)

from support import config_support_class
config = config_support_class.config_support_class(inventory)

if __name__ == '__main__':
    info = config.getMidspanInfo(tiles)
	
    for tile in info:
        tileName = tile[0]
        midspanIp = tile[2]
        poePort = tile[3]

        if action == 0:
            # check if tile is on
            status, _ = midspan.getPortStatus(midspanIp, poePort)
            
            # check how much power it draws
            if status == 1:
                power, _, _ = midspan.getPortPower(midspanIp, poePort)
                if power > 7:
                    print("Power draw = " + str(power) + ". Something is still on, but proceeding anyway... yolo!")
                status = midspan.setPortOnOff(midspanIp, poePort, action)
                if status == 0:
                    print(tileName + " powered down.")
                else:
                    print("ERROR: Could not power down " + tileName + ".")
            else:
                print(tileName + " is already off.")

        else:
            # check if tile is on
            status, _ = midspan.getPortStatus(midspanIp, poePort)
            
            # check how much power it draws
            if status == 0:
                status = midspan.setPortOnOff(midspanIp, poePort, action)
                if status == 1:
                    print(tileName + " powering up.")
                else:
                    print("ERROR: Could not power up " + tileName + ".")
            else:
                print(tileName + " is already on.")
