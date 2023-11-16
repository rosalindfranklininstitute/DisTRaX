# DisTRaX

* To read the documentation, [visit the project website](https://rosalindfranklininstitute.github.io/DisTRaX/).

## Scientific Background

DisTRaX is a fast and scalable deployment tool to create quick and efficient storage systems onto high-performance computing (HPC) compute nodes utilising the compute node's system memory/storage. It can scale to the arbitrary size of the HPC job to reduce the I/O overhead and processing times of I/O bound applications.

Please follow the [install guide](https://rosalindfranklininstitute.github.io/DisTRaX/user/tutorials/install.html) and  [quick start guide](https://rosalindfranklininstitute.github.io/DisTRaX/user/tutorials/quickstart.html) to get started and see how to it can reduce the processing times of your applications. Please follow the  [quick start guide MPI](https://rosalindfranklininstitute.github.io/DisTRaX/user/tutorials/quickstart_mpi.html) to run DisTRaX at scale.


## Would my software benefit from using this

More than likely, especially in the case where your application is I/O bound, as this will allow you to leverage the RAM on the HPC node as shared storage and thus will more than likely rate limited by the HPC network rate and not the storage write rate. However, DisTRaX can also potentially reduce the time for compute-bound operations that need to read data to do processing, such as [RELION](https://relion.readthedocs.io/), as having the data in the shared RAM will reduce the read time.

DisTRaX can also, in a cloud cluster setting, help reduce cost overheads as if the data fits into the RAM of the compute nodes, it can remove the need for a fast central filesystem.

In short, DisTRaX allows you to use existing compute infrastructure to speed up your software while requiring no changes to your existing software.

## Example

This example shows how easy it is to use DisTRaX with your existing software.

```bash
#! /bin/bash
#SBATCH --job-name=distrax_example
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=1
#SBATCH --time=10:00

# Get hostnames
hostnames=`scontrol show hostnames| sed -n -e 'H;${x;s/\n/,/g;s/^,//;p;}'`

# Get number of hosts
number_of_hosts=`scontrol show hostnames | wc -l`

# Create Storage System
mpirun -np $number_of_hosts --host $hostnames distrax_mpi -c distrax.cfg -a create

# Move data to storage cluster
rsync input_data_location /mnt/distrax/

# Run Application
./Heavy-IO-application --input_dir /mnt/distrax --output_dir /mnt/distrax

# Move data off storage cluster
rsync /mnt/distrax permanent_output_data_location

# Remove Storage System
mpirun -np $number_of_hosts --host $hostnames distrax_mpi -c distrax.cfg -a remove

```
