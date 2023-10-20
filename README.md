# Fleet management Ansible playbooks for Techtile Raspberry Pis

## Hosts/Tiles
Host inventory: `inventory/hosts.yaml`  

The inventory defines different children groups of all hosts based on hosts location/function.
* **server**: Techtile server, the `ansible_user` variable value may need to be changed to another user account.
* **tests**: Rpi hosts used for testing.
* **wallEast, wallWest**: Configugreen and accessible Rpi hosts mounted on east and west walls.
* **segmentA -- segmentG**: Configured and accessible Rpi hosts grouped by segments A -- G.
* **multiON**: Add any hosts to this group, playbook `start_receiver_multi.yaml` starts the receivers of Rpis within this group.
* **rpis**: parent group of wallEast and wallWest, contains all the Rpis have been configured and accessible
* **fail**: hosts within this group are currently not accessible. Move the hosts to wallEast/wallWest and corresponding segment groups once they become accessible and get configured. 

Layout of Current Rpis (Red tile: inaccessible, Green tile: accessible and configured)
![layour](./Layout.png)

## Example server/client files
* `server/`: Source files in Python for techtile server, starting PUSH, PUB and ROUTER zeroMQ servers to distributing tasks, sending killing message and receiving results from clients(rpis). Three alternatives to start the server.
* `client/`: Source files in Python for all rpis, connecting to each zeroMQ server for receiving tasks, killing signals and sending results. 

To copy all files to rpis and the server, run:
```
ansible-playbook -i inventory/hosts.yaml copy-scripts.yaml
```
The playbook ` copy-scripts.yaml` copies `src/client` to `/home/pi/client` on all Rpis, and `src/server` to `/home/techtile/server`. The destination path of server `/home/techtile/server` may need to be changed depends on the user account that is used on the server.  
To only copy the client scripts:
```
ansible-playbook -i inventory/hosts.yaml -l rpis copy-scripts.yaml
``` 
To only copy the server scripts:
```
ansible-playbook -i inventory/hosts.yaml -l server copy-scripts.yaml
``` 
To only copy to a specific Rpis host (A01 for example):
```
ansible-playbook -i inventory/hosts.yaml -l A01 copy-scripts.yaml
``` 