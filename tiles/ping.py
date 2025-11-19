# Ping

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
ansible_yaml_file = "ping.yaml"
tiles = "ceiling"

if __name__ == '__main__':

    print(exp_dir)

    #   Check or copy files to the clients
    r = ansible_runner.run(
        inventory=f"{exp_dir}/inventory/hosts.yaml",
        playbook=f"{exp_dir}/general/{ansible_yaml_file}",
        extravars={"tiles": f"{tiles}"}
    )
