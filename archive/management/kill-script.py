# Kill script

# *** Includes ***
import os

# Get the current directory of the script
server_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate one folder back to reach the parent directory
exp_dir = os.path.abspath(os.path.join(server_dir, os.pardir))

import time 
import ansible_runner

#   INFO
server_user_name = "jarne"
ansible_yaml_file = "experiments/kill_script.yaml"
tiles = "ceiling"

script_name = "tx_waveforms_random_phase.py"

if __name__ == '__main__':

    #   Check or copy files to the clients
    r = ansible_runner.run(
        inventory=f"/home/{server_user_name}/Documents/GitHub/ansible/inventory/hosts.yaml",
        playbook=f"/home/{server_user_name}/Documents/GitHub/ansible/{ansible_yaml_file}",
        extravars={"tiles": f"{tiles}", "script_name": f"{script_name}"}
    )
