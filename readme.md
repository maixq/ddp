### DDP
Welcome to this repository on distributed training!

Distributed training is a technique used to train deep learning models across multiple machines or nodes, rather than on a single machine. This approach allows for faster training times, increased model capacity, and the ability to tackle larger datasets.

### Set up
To begin, mfa to AWS on your local machine to ensure access to S3 for downloading the data folder.

Next, create the master and worker nodes by running: 

```python

# create nodes
python py_scripts/create_nodes.py

# cd tf
terraform apply
```

You can check your AWS console to ensure that the instances are created successfully.
