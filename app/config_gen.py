# -*- coding: utf-8 -*-
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from yaml.representer import SafeRepresenter

class StringValueDumper(Dumper):
    def represent_str(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', data, style='"')

StringValueDumper.add_representer(str, StringValueDumper.represent_str)
splash = """
                                   /##                                                        
                                  #/ ###   #                                                   
                                 ##   ### ###                                                  
                                 ##        #                                                   
                                 ##                                                            
   /###      /###   ###  /###    ######  ###       /###            /###      /##  ###  /###    
  / ###  /  / ###  / ###/ #### / #####    ###     /  ###  /       /  ###  / / ###  ###/ #### / 
 /   ###/  /   ###/   ##   ###/  ##        ##    /    ###/       /    ###/ /   ###  ##   ###/  
##        ##    ##    ##    ##   ##        ##   ##     ##       ##     ## ##    ### ##    ##   
##        ##    ##    ##    ##   ##        ##   ##     ##    u  ##     ## ########  ##    ##   
##        ##    ##    ##    ##   ##        ##   ##     ##    n  ##     ## #######   ##    ##   
##        ##    ##    ##    ##   ##        ##   ##     ##    d  ##     ## ##        ##    ##   
###     / ##    ##    ##    ##   ##        ##   ##     ##    e  ##     ## ####    / ##    ##   
 ######/   ######     ###   ###  ##        ### / ########    r   ########  ######/  ###   ###  
  #####     ####       ###   ###  ##        ##/    ### ###   s     ### ###  #####    ###   ### 
                                                        ###  c          ###                    
                                                  ####   ### o    ####   ###                   
                                                /######  /#  r  /######  /#                    
                                               /     ###/    e /     ###/                      

""" 

print(splash)

print("Reading input file... apps.yml")
print("")

with open('apps.yml') as f:
    apps = load(f, Loader=Loader)

print("Generating config files... from the following app.yml")
print(dump(apps, Dumper=Dumper))

service_names = []
for app in apps:
    # get first key of every app
    service_names.append(list(app.keys())[0])

# make an empty map
docker_compose_out = {"services": {}}

# iterate over the apps
for app in apps:
    # get the service name
    service_name = list(app.keys())[0]
    # get the service config
    service_config = app[service_name]
    # add the service config to the docker-compose map
    docker_compose_out["services"][service_name] = service_config['docker_compose']
    env_vars = app[service_name]["env"]
    docker_compose_out["services"][service_name]["image"] = service_config['image']  
    docker_compose_out["services"][service_name]["environment"] = env_vars
    ports = []
    for port in app[service_name]["ports"]:
        ports.append(f"{port['source']}:{port['target']}")
    docker_compose_out["services"][service_name]["ports"] = ports
print("Generating docker-compose.yml")
docker_compose_file_contents = dump(docker_compose_out, Dumper=StringValueDumper)

with open('docker-compose.yml', 'w') as f:
    f.write(docker_compose_file_contents)

print("docker-compose.yml generated")

print("Generating akash-sdl.yml")

akash_sdl_out = {"version": "2.0", "services": {}}

for app in apps:
    service_name = list(app.keys())[0]
    service_config = app[service_name]
    akash_sdl_out["services"][service_name] = service_config['akash']
    env_vars = app[service_name]["env"]
    akash_sdl_out["services"][service_name]["env"] = env_vars
    ports = []
    for port in app[service_name]["ports"]:
        ports.append({"number": port["source"], "protocol": "TCP"})
    akash_sdl_out["services"][service_name]["expose"] = ports

with open('akash-sdl.yml', 'w') as f:
    f.write(dump(akash_sdl_out, Dumper=StringValueDumper))

print("akash-sdl.yml generated")