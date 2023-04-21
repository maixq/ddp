import json
import os
import logging

def get_ip(tf_dir):
    
    tf_path = os.path.join(tf_dir, "terraform.tfstate")
    
    if not os.path.exists(tf_path):
        logging.warning('No tfstate file!')
        
    f = json.load(open(tf_path))
    

    for i in f["resources"]:
        if i["mode"] == "managed" and i["type"] == "aws_instance":
            instances = i["instances"]

    ip_addresses = []

    if instances:
        for instance in instances:
            ip_addresses.append(instance["attributes"]["public_ip"])

    return ip_addresses