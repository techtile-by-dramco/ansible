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

Layout of Current Rpis (Red tile: unaccessible, Green tile: accessible and configured)

wallEast:
<table>
 <tr>
    <td style="width:100px; height:30px;background-color:green;"> A01</td>
    <td style="width:100px; height:30px;background-color:green;"> B01</td>
    <td style="width:100px; height:30px;background-color:green;"> C01</td>
    <td style="width:100px; height:30px;background-color:green;"> D01</td>
    <td style="width:100px; height:30px;background-color:green;"> E01</td>
    <td style="width:100px; height:30px;background-color:green;"> F01</td>
    <td style="width:100px; height:30px;background-color:green;"> G01</td>
  </tr>
 <tr>
    <td style="width:100px; height:30px;background-color:green;"> A02</td>
    <td style="width:100px; height:30px;background-color:green;"> B02</td>
    <td style="width:100px; height:30px;background-color:red;"> C02</td>
    <td style="width:100px; height:30px;background-color:green;"> D02</td>
    <td style="width:100px; height:30px;background-color:green;"> E02</td>
    <td style="width:100px; height:30px;background-color:green;"> F02</td>
    <td style="width:100px; height:30px;background-color:green;"> G02</td>
  </tr>
 <tr>
    <td style="width:100px; height:30px;background-color:green;"> A03</td>
    <td style="width:100px; height:30px;background-color:green;"> B03</td>
    <td style="width:100px; height:30px;background-color:green;"> C03</td>
    <td style="width:100px; height:30px;background-color:green;"> D03</td>
    <td style="width:100px; height:30px;background-color:green;"> E03</td>
    <td style="width:100px; height:30px;background-color:green;"> F03</td>
    <td style="width:100px; height:30px;background-color:green;"> G03</td>
  </tr>
 <tr>
    <td style="width:100px; height:30px;background-color:green;"> A04</td>
    <td style="width:100px; height:30px;background-color:green;"> B04</td>
    <td style="width:100px; height:30px;background-color:green;"> C04</td>
    <td style="width:100px; height:30px;background-color:green;"> D04</td>
    <td style="width:100px; height:30px;background-color:green;"> E04</td>
    <td style="width:100px; height:30px;background-color:green;"> F04</td>
    <td style="width:100px; height:30px;background-color:green;"> G04</td>
  </tr>
</table>


wallWest:
<table>
 <tr>
    <td style="width:100px; height:30px; background-color:green;"> A11</td>
    <td style="width:100px; height:30px; background-color:green;"> B11</td>
    <td style="width:100px; height:30px; background-color:green;"> C11</td>
    <td style="width:100px; height:30px; background-color:green;"> D11</td>
    <td style="width:100px; height:30px; background-color:red;"> E11</td>
    <td style="width:100px; height:30px; background-color:green;"> F11</td>
    <td style="width:100px; height:30px; background-color:green;"> G11</td>
  </tr>
 <tr>
    <td style="width:100px; height:30px; background-color:red;"> A12</td>
    <td style="width:100px; height:30px; background-color:green;"> B12</td>
    <td style="width:100px; height:30px; background-color:red;"> C12</td>
    <td style="width:100px; height:30px; background-color:green;"> D12</td>
    <td style="width:100px; height:30px; background-color:green;"> E12</td>
    <td style="width:100px; height:30px; background-color:green;"> F12</td>
    <td style="width:100px; height:30px; background-color:red;"> G12</td>
  </tr>
 <tr>
    <td style="width:100px; height:30px; background-color:red;"> A13</td>
    <td style="width:100px; height:30px; background-color:green;"> B13</td>
    <td style="width:100px; height:30px; background-color:green;"> C13</td>
    <td style="width:100px; height:30px; background-color:green;"> D13</td>
    <td style="width:100px; height:30px; background-color:green;"> E13</td>
    <td style="width:100px; height:30px; background-color:green;"> F13</td>
    <td style="width:100px; height:30px; background-color:red;"> G13</td>
  </tr>
 <tr>
    <td style="width:100px; height:30px; background-color:red;"> A14</td>
    <td style="width:100px; height:30px; background-color:green;"> B14</td>
    <td style="width:100px; height:30px; background-color:green;"> C14</td>
    <td style="width:100px; height:30px; background-color:green;"> D14</td>
    <td style="width:100px; height:30px; background-color:green;"> E14</td>
    <td style="width:100px; height:30px; background-color:green;"> F14</td>
    <td style="width:100px; height:30px; background-color:red;"> G14</td>
  </tr>
</table>