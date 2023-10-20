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
* `server/`: Source files in Python for techtile server, starting PUSH, PUB and ROUTER zeroMQ servers to distributing tasks, receiving results and sending killing message to clients(rpis). Three alternatives to start the server.
* `client/`: Source files in Python for all rpis, connecting to each zeroMQ server for receiving tasks, sending results and receiving killing signals. 

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

## Start usrp receivers on Rpis
There are few ways to start the receivers on Rpis
### Start receivers by wall
By default, all Rpis on wallEast connect to zeroMQ servers binding port 5555-5557, all Rpis on wallWest connects to zeroMQ servers binding port 6555-6557. 
```
{
    wallEast: 5555-5557
    wallWest: 6555-6557
}
```
This can be changed in `inventory/group_vars/wallEast.yaml` and `inventory/group_vars/wallWest.yaml`, the `port` value.  
**NOTE**: If port value is changed to 1000 for instance, the clients will connect to zeroMQ servers on 1000, 1001 and 1002 for different message and functions.
* To Start receivers on both walls
```
ansible-play -i inventory/hosts.yaml start_receiver_walls.yaml
```
* To Start receivers on one wall
```
ansible-play -i inventory/hosts.yaml --tags wallEast start_receiver_walls.yaml
```
The playbook will start the clients on the Rpis to listen to the server for task distribution. It will also generate a config file and send to the server at `server/server_config.yaml`, indicating the raspberry Rpis on which walls are on, how many Rpis have successfully start listening on each wall.  
### Start receivers by segments
Default ports used by each segment:
```
{
    segmentA: 5555-5557,
    segmentB: 6555-6557,
    segmentC: 7555-7557,
    segmentD: 8555-8557,
    segmentE: 9555-9557,
    segmentF: 10555-10557,
    segmentG: 11555-11557,
}
```
* To Start receivers on all segments
```
ansible-play -i inventory/hosts.yaml start_receiver_segments.yaml
```
* To Start receivers on specific segments (segmentA and segmentB for example)
```
ansible-play -i inventory/hosts.yaml --tags segmentA,segmentB start_receiver_segments.yaml
```
The playbook will start the clients on the Rpis of underlying segments to listen to the server for task distribution. It will also generate a config file and send to the server at `server/server_config.yaml`, indicating the raspberry Rpis in which segment are on, how many Rpis have successfully start listening in that segment. 

### Start receivers by choice
You can change in `inventory/hosts.yaml`, under the `multiON` group, put the Rpis host names of that you want to start. And run:
```
ansible-play -i inventory/hosts.yaml start_receiver_multi.yaml
```
In this case, all chosen Rpis will start the receivers and listen to port 5555-5557

### Rescue the Pis
Sometimes Ansible will give unreachable errors on some Rpis `ssh could not resolve host name ...`. This is mostly like due to the connection to the DNS server. One solution for this is to put the IP addresses for all the hosts in the inventory, so Ansible does not need to query the DNS server each time it tries to connect to the remote host. This method can only be used if the IP addresses of Rpis are static.  
If this error occurs on one Rpis, the `server_config.yaml` will not include the connections of the failed Rpis, and the server will expect less connected Rpis listening to its task.  
If you want to make sure all Rpis are connected, you can manually start the Rpis receiver by using: (for example to manually start the Pis receiver on A01, B02 and C11)
```
ansible-play -i inventory/hosts.yaml -l A01,B02,C11 start_receiver_rescue.yaml
```
**NOTE: This rescue playbook will start the designated Pis receiver and make them listen to ports 5555-5557 by default. However, this does not change `server_config.yaml` on the server side, so you need to go the server, change the `server/server_config.yaml`, add the number of manually started Pis to `connections` value under `wallEast` or `segmentA` (Since they are the groups listening to port 5555-5557 by default.)**  
**If `wallEast` or `segmentA` does not exist in the `server_config.yaml`, or you want to force the rescued Pis to listen to another port group, you can use the following command:**
```
ansible-playbook -i inventory/hosts.yaml -l  A01,B02,C11 --extra-vars "port=6555" start_receiver_rescue.yaml
```
**This command starts receivers on A01, B02 and C11, force them to listen to port 6555-6557. In this case, you need to add 3 to the connection value of `wallWest` or `segmentB` in  `server/server_config.yaml` on the server side.**

