# BirdNet Mini

Proof of concept implementation of BirdNet for monitoring bird populations using audio recordings. It's designed to be run on a Raspberry Pi >=4 with at least 4GB of RAM.

# Development

You may develop the software directly on the Raspberry Pi. However, it's recommended to develop on a more powerful machine and then deploy the software to the Raspberry Pi.


## Environment
If you develop on a standard PC use miniconda to create a new Python environment.

Create a new conda environment using the provided `environment.yml` file.

```bash
conda env create -f environment.yml
```

# Deployment

## Prepare the Raspberry Pi

The demo system consists of a fresh installation of Raspberry Pi OS.

### Install required packages

In order to make the pyaudio package to be installable, install portaudio19-dev package

```bash
$ sudo apt-get install portaudio19-dev
```

### Clone the software

```bash
$ git clone  https://github.com/Science-Camp-TUI/birdnet-mini.git
```

### Create a runtime environment and install the required packages

```bash
$ python3 -m venv birdnet-mini
```

Activate the virtual environment

```bash
$ source birdnet-mini/bin/activate
```

### Install the required packages

```bash
$ pip install -r requirements_rpi.txt
```

### Running

The software transmits the bird classifications via serial port. If no serial port is available, the software simulates the transmission.

You may attach a Lora or MiOTY module to the Raspberry Pi serial for IoT transmission. 

Activate the environment set the `PYTHONPATH` to the root of the project with `export PYTHONPATH=$(pwd)` 

#### File mode

To run the software in file mode, put the audio files and (optionally) a metadata file in a folder (e.g. `~/bird-recordings`). and then run the software with:

```bash 
(birdnet-mini) $ python -m birdnet_mini.main --audio-folder ~/bird-recordings --metadata-file ~/bird-recordings/SMM11597_Summary.txt --serial-port /dev/ttyACM0
```

Without metadata file, timestamp will be set to the current time and latitude and longitude to the default values.

#### Live mode

For live you may list available audio devices with:

```bash
(birdnet-mini) $ python -m birdnet_mini.main --list-devices
```
Then run the software with:

```bash 
(birdnet-mini) $ python -m birdnet_mini.main --live --device-index 1 --serial-port /dev/ttyACM0
```