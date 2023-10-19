# Fleet management Ansible playbooks for Techtile raspberry Pis

## Hosts/Tiles
Host inventory: `inventory/hosts.yaml`

The inventory defines different children groups of all hosts based on hosts location/function.
* server: Techtile server, the `ansible_user` variable value may need to be changed to another user account.
* tests: Rpi hosts used for testing.
* wallEast, wallWest: Configugreen and accessible Rpi hosts mounted on east and west walls.
* segmentA -- segmentG: Configured and accessible Rpi hosts grouped by segments A -- G.
* multiON: Add any hosts to this group, playbook `start_receiver_multi.yaml` starts the receivers of Rpis within this group.
* rpis: parent group of wallEast and wallWest, contains all the Rpis have been configured and accessible
* fail: hosts within this group are currently not accessible. Move the hosts to wallEast/wallWest and corresponding segment groups once they become accessible and get configured. 

Layout of Current Rpis (Red tile: inaccessible, Green tile: accessible and configured)
![layour](./Layout.png)