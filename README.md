# BirdNet Mini

Proof of concept implementation of BirdNet for monitoring bird populations using audio recordings. It's designed to be run on a Raspberry Pi >=4 with at least 4GB of RAM.

# Development

You may develop the software directly on the Raspberry Pi. However, it's recommended to develop on a more powerful machine and then deploy the software to the Raspberry Pi.


## Environment
If you develop on a standard PC use miniconda to create a new Python environment.

```bash
Create a new conda environment using the provided `environment.yml` file.

```bash
conda env create -f environment.yml
```
# Deployment

## Prepare the Raspberry Pi

The demo system consists of a fresh installation of Raspberry Pi OS.

We use TensorflowLite as Runtime on the Raspberry Pi. Follow the documentation at https://pimylifeup.com/raspberry-pi-tensorflow-lite/

## Copy Simulation data

To be done...


## Deploy the software

To deploy the software to the Raspberry Pi. Clone the repository there. 
then install the required packages using the provided `requirements.txt` file.

```bash
$ pip install -r requirements.txt
```

