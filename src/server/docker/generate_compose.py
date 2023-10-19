from jinja2 import Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('docker-compose-template.j2')

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

compose_config = {
    'services': {}
}
service_temp = {
    'image': 'central-server',
    'ports': [],
    'command': [],
}

servers = config['servers']
for server in servers:
    service_var = service_temp.copy()
    port = port_match_wall[server['name']]
    command = ["python3", "-u", "central_server.py", "--port", str(port), "--connections", str(server['connections'])]
    service_var['command'] = command
    ports = '{}-{}:{}-{}'.format(port, port+2, port, port+2)
    service_var['ports'] = [ports]
    new_service = {server['name']: service_var}
    compose_config['services'].update(new_service)


output = template.render(compose_config)

with open('docker-compose.yaml', 'w') as f:
    f.write(output)
