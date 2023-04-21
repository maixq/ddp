
import json

def get_gpu_ip():
    configuration = []
    instance_types = {
        "1": ['g4dn.xlarge']
    }
    gpu_d = {}

    while True:
        d = {}
        node_type = input('master/worker: ')
        application_name = "cv-ddp-" + node_type + "-node"
        num_nodes = int(input('Number of nodes for this server: '))
        instance_type = input('choose your instance type: ')
        if instance_type in instance_types.values():
            gpu_num = [ k for k, v in instance_type.items() if v == instance_type[0]]
            gpu_d[instance_type] = gpu_num
        else:
            gpu_d[instance_type] = 0

        # default config
        d["application_name"] = application_name
        d["no_of_instances"] = num_nodes
        d['instance_type'] = instance_type
        d["ami"] = "ami-0184e674549ab8432"
        d["vpc_security_group_ids"] = ["sg-08794d9db5775686a"]
        d["subnet_id"] = "subnet-e86473a5"
        d["key_name"] = "xueqiao"
        d["iam_instance_profile"] = "carro-ds-cv-training-role"
        
        # append to config list
        configuration.append(d)
 
        add_more = input('Add another instance? y/n ')
        if add_more in ['Yes','yes','y','Y']:
            pass
        else:
            break
    return configuration, gpu_d
    
if __name__ == "__main__":

    configuration, gpu_d = get_gpu_ip()
    with open('../tf/test.tfvars', 'w') as f:
        f.write('region = "us-east-1"' + '\n' + 'configuration = ' +  json.dumps(configuration, indent=4))
    



    
    
    
        
    
    
    
    
    

