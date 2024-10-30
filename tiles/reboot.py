# Reboot

# *** Includes ***
import os

# Get the current directory of the script
server_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate one folder back to reach the parent directory
exp_dir = os.path.abspath(os.path.join(server_dir, os.pardir))

import ansible_runner

#   INFO
server_user_name = "techtile"
ansible_yaml_file = "shutdown.yaml"
tiles = "wallEast"
action_to_take = "reboot"
timeout_minutes = 0 # timeout in minutes!

if __name__ == '__main__':

    # Run ansible
    r = ansible_runner.run(
        inventory=f"/home/{server_user_name}/ansible/inventory/hosts.yaml",
        playbook=f"/home/{server_user_name}/ansible/tiles/{ansible_yaml_file}",
        extravars={"tiles": f"{tiles}", "action_to_take": f"{action_to_take}", "timeout_seconds": (timeout_minutes * 60)}
    )
    