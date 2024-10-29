# Clean up "exp" directory for the specified clients (or hosts) (or tiles)

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
ansible_yaml_file = "load-fpga-image.yaml"
tiles = "E09"

if __name__ == '__main__':

    #   Check or copy files to the clients
    r = ansible_runner.run(
        inventory=f"/home/{server_user_name}/ansible/inventory/hosts.yaml",
        playbook=f"/home/{server_user_name}/ansible/{ansible_yaml_file}",
        extravars={"tiles": f"{tiles}"}
    )
