from configure_ec2 import get_gpu_ip
import json
import logging
import subprocess
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

terraform_path = '/home/ubuntu/Users/maixueqiao/ddp/tf'
terraform_cmds = ['terraform init', 'terraform plan -var-file=test.tfvars -out ddpplan.out']


PROJECT_NAME = "ddp"
REGION = "us-east-1"
OWNER = "xueqiao"
TEAM = "cv"

dir_path = '/home/ubuntu/Users/maixueqiao/'+ PROJECT_NAME + '/tf'

# get ec2 config and num of gpus of respective instance
configuration, gpu_d = get_gpu_ip()
with open('/home/ubuntu/Users/maixueqiao/ddp/tf/test.tfvars', 'w') as f:
    f.write('region = \"' + REGION + '\"' + '\n' 
        + 'mytags = {' + '\n'
        + 'project = \"' + PROJECT_NAME + '\"' + '\n' 
        + 'owner = \"' + OWNER + '\"' + '\n' 
        + 'team = \"' + TEAM + '\"' + '\n' 
        + '}' + '\n'
        + 'configuration = ' +  json.dumps(configuration, indent=4))
logging.info('EC2 config is written into tfvars file successfully! ')

response = input("Proceed with creating nodes? y/n: ")
if response == 'n':
    print('Abandon project')
elif response == 'y':
    logging.info('Creating nodes with terraform.. ')

    for cmd in terraform_cmds:
        print(cmd)
        output = subprocess.check_output(cmd.split(), cwd=terraform_path)
        print(output.decode('utf-8'))

