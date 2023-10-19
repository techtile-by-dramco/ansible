import yaml

port_match_wall = {
    "wallEast": 5555,
    "wallWest": 6555,
    "segmentA": 5555,
    "segmentB": 6555,
    "segmentC": 7555,
    "segmentD": 8555,
    "segmentE": 9555,
    "segmentF": 10555,
    "segmentG": 11555,
}

try:
    with open("../server_config.yaml", "r") as f:
        config = yaml.safe_load(f)
except FileExistsError:
    print("No original config file exits, make sure you have run ansible to start all receivers")

servers = config['servers'].copy()
print(servers)
for server in servers:
    server.update({'port': port_match_wall[server['name']]})

new_conf = {}
new_conf["servers"] = servers
with open('config.yaml', 'w') as outfile:
    yaml.dump(new_conf, outfile, default_flow_style=False)