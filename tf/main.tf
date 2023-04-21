terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 4.16"
        }
    }
    required_version = ">= 1.2.0"
}

provider "aws" {
    region = var.region
}

locals {
    serverconfig = [
        for server in var.configuration : [
            for i in range(1, server.no_of_instances+1) : {
                # reference to ec2 attribute
                instance_name = "${server.application_name}-${i}"
                ami = server.ami
                instance_type = server.instance_type
                subnet_id = server.subnet_id
                security_groups = server.vpc_security_group_ids
                key_name = server.key_name
                iam_instance_profile = server.iam_instance_profile
            }
        ]
    ]
}

locals {
    instances = flatten(local.serverconfig)
}

resource "aws_instance" "ddp-instance" {
    for_each = { for server in local.instances: server.instance_name => server}
    
    ami = each.value.ami
    instance_type = each.value.instance_type
    vpc_security_group_ids = each.value.security_groups
    subnet_id = each.value.subnet_id
    key_name = each.value.key_name
    iam_instance_profile = each.value.iam_instance_profile

    user_data = <<EOF
    #!/bin/bash
    echo "Copying SSH key to master and worker nodes"
    echo -e "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCWYaUN8RgxwKXBL1SafEziy6u786kAb+TupmQfpFSiGZ8DzVtqWYvuo9PvMExTjye3Z5wX6rRdPDNQtO1ehJhA+6K6NPipY/zLLfUpZQ2+8KAuQqXGqTdSV2A3N8ZJLPYBUgl00EEypw5Vi1nK7QjxkCKQpQKwJkd380XI8IHJKl9maOOIloGzMhMzHx1vvk3vjR7eArhnNOxozGCMi91sRyIS1UldfUBRhyhe1sfRagwhvg+vQNUiPCwSeuOG0BTeWzZBcLV2BTSeyNPW9UAx/Ggxk9H407b3Z0PXrqjVxXBnRhn1I9Kof+jvSpKUYK9c0jUtCAkyyrSfmlW+NkDp xueqiao" >> /home/ubuntu/.ssh/authorized_keys
    
    echo "Copying hostname to ${each.value.instance_name}"
    hostname ${each.value.instance_name}
    echo "${each.value.instance_name}" > /etc/hostname
    EOF
    
    tags = merge(
        {Name = "${each.value.instance_name}"},
        {Node_type = split("-", "${each.value.instance_name}")[2]},
        var.mytags
    )

    provisioner "local-exec" {
        command = <<-EOT
            echo "[${self.tags.Node_type}]\n ${self.public_ip}" | sed 's/\-e//g' >> aws_hosts && aws ec2 wait instance-status-ok --instance-ids ${self.id} --region us-east-1
        EOT
    }
}

# set up null resource to execute ansible once after all instances have spinned up
resource "null_resource" "ddp" {
  depends_on = [
    aws_instance.ddp-instance
  ]
  provisioner "local-exec" {
    command = "ansible-playbook -i aws_hosts --key-file /home/ubuntu/Users/maixueqiao/xueqiao.pem /home/ubuntu/Users/maixueqiao/ddp/ansible/ansible-playbook.yml"
  }
}

output "instances" {
    value = "${aws_instance.ddp-instance}"
    description = "All Machine details"
}

# general variables
variable "region" {
  description = "The AWS region in which to create resources."
  type        = string
  default     = "us-east-1"
}

variable "mytags" {
    type = map
}