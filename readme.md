### DDP
Welcome to this repository on distributed training!

Distributed training is a technique used to train deep learning models across multiple machines or nodes, rather than on a single machine. This approach allows for faster training times, increased model capacity, and the ability to tackle larger datasets.

### Set up
1. To begin, mfa to AWS on your local machine to ensure access to S3 for downloading the data folder.

2. Next, create the master and worker nodes by running: 

```python

# create nodes
python py_scripts/create_nodes.py

# cd tf
terraform apply "ddpplan.out"

```

You can check your AWS console to ensure that the instances are created successfully.

3. Run anisble playbook to download data from s3
Ensure that the data has been correctly uploaded to your s3 bucket with corresponding paths.

You can adjust the source of s3 bucket by changing the following in download_s3_data.yml playbook.

```python

      # Set the name of the S3 bucket
    - s3_bucket_name: "{name of s3}"
      # Set the prefix for the S3 objects to download
    - s3_object_prefix: "{prefix for the S3 objects}"
      # Set the local destination directory for the downloaded files
    - local_dir_path: "{local destination directory}"

```

```python
 ansible-playbook -i aws_hosts --key-file {key_name}.pem ../ansible/download_s3_data.yml

```

4. Set up detectron2 environment

```python
# /tf 
 ansible-playbook -i aws_hosts --key-file {key_name}.pem ../ansible/detectron.yml

```

5. Git clone training code 
Update training parameters in the config files and push to github before cloning to master and worker nodes.

```python
ansible-playbook -i aws_hosts --key-file {key_name}.pem ../ansible/git_clone.yml

```

