# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from yaml import load, dump

load_dotenv()

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
    docker_compose_out["services"][service_name]["image"] = f"{service_config['image']}:{os.environ['VERSION']}"  
    docker_compose_out["services"][service_name]["environment"] = env_vars
    ports = []
    for port in app[service_name]["ports"]:
        ports.append(f"{port['source']}:{port['target']}")
    docker_compose_out["services"][service_name]["ports"] = ports
print("Generating docker-compose.yml")
docker_compose_file_contents = dump(docker_compose_out, Dumper=Dumper)

with open('docker-compose.yml', 'w') as f:
    f.write(docker_compose_file_contents)

print("docker-compose.yml generated")

print("Generating akash-sdl.yml")

placement = {
                    "akash":
                        {
                            "attributes": 
                                {
                                    "host": "akash"
                                },
                            "signedBy": 
                                {
                                    "anyOf": 
                                        [
                                            "akash1365yvmc4s7awdyj3n2sav7xfx76adc6dnmlx63",
                                            "akash18qa2a2ltfyvkyj0ggj3hkvuj6twzyumuaru9s4"
                                        ]
                                },
                            "pricing": { }
                        }
                
                }

akash_sdl_out = {
                    "version": "2.0", 
                    "services": {}, 
                    "profiles": 
                        {
                            "compute": {}, 
                            "placement": placement
                        },
                    "deployment": {}
                }

for app in apps:
    service_name = list(app.keys())[0]
    service = {service_name: {}}
    service[service_name]['image'] = f"{app[service_name]['image']}:{os.environ['VERSION']}"
    resolved_env_vars = {}
    for key, value in env_vars.items():
        if key in os.environ:
            resolved_env_vars[key] = os.environ[key]
        else:
            resolved_env_vars[key] = value
    array_of_env_var_strings = []
    for key, value in resolved_env_vars.items():
        array_of_env_var_strings.append(f"{key}='{value}'")
    service[service_name]['env'] = array_of_env_var_strings
    exposed_ports = []
    for port in app[service_name]['ports']:
        exposed_ports.append({"port": port['source'], "to": [{'global': port['global']}]})
    service[service_name]['expose'] = exposed_ports
    akash_sdl_out['services'][service_name] = service[service_name]
    compute =   {
                    "resources": 
                        {
                            "cpu": app[service_name]['akash']['compute']['cpu'], 
                            "memory": app[service_name]['akash']['compute']['memory'], 
                            "storage": app[service_name]['akash']['compute']['storage']
                        }       
                }
    akash_sdl_out['profiles']['compute'][service_name] = compute
    pricing =   {
                    "amount": app[service_name]['akash']['placement']['pricing']['amount'], 
                    "denom": app[service_name]['akash']['placement']['pricing']['denom']
                }
    akash_sdl_out['profiles']['placement']['akash']['pricing'][service_name] = pricing
    deployment =    {
                        "akash":
                            {
                                "profile": service_name, 
                                "count": app[service_name]['akash']['deployment']['count']
                            }
                    }
    akash_sdl_out['deployment'][service_name] = deployment

with open('akash-sdl.yml', 'w') as f:
    f.write(dump(akash_sdl_out, Dumper=StringValueDumper))

print("akash-sdl.yml generated")