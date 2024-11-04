# Give shutdown command to host

# *** Includes ***
import ansible_runner

#   INFO
server_user_name = "techtile"
ansible_yaml_file = "shutdown.yaml"
tiles = "G01"
action_to_take = "shutdown"
timeout_minutes = 0 # timeout in minutes!

if __name__ == '__main__':

    # Run ansible
    r = ansible_runner.run(
        inventory=f"/home/{server_user_name}/ansible/inventory/hosts.yaml",
        playbook=f"/home/{server_user_name}/ansible/tiles/{ansible_yaml_file}",
        extravars={"tiles": f"{tiles}", "action_to_take": f"{action_to_take}", "timeout_seconds": (timeout_minutes * 60)}
    )
    