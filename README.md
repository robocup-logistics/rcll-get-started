# rcll-get-started
This repository bundles the documentation and setup details around the software used in the RCLL.
### General information

Most of the software used in the RCLL can be found in the [github organization](https://github.com/robocup-logistics). 
The docker images for the RCLL get published to the [quay](https://quay.io/organization/robocup-logistics).
#### Rules for RCLL
The rulebook for the RCLL can be found [here](https://github.com/robocup-logistics/rcll-rulebook).
#### Libraries for RCLL
There are various libraries to make communication with the refbox easy, at the moment there is one for [Java](https://github.com/robocup-logistics/rcll-java) and one for [C++](https://github.com/fawkesrobotics/protobuf_comm).


### Installation
##### Prerequisites
To use this repository you have to have `docker`, `docker-compose` and `bash` installed. To make the commands available you have to source `setup.sh`, you can do this in our local 
`~/.bashrc`

### Configuration
All the commands that are listened below can be configured via various env variables. To overwrite the defaults which are set in the `setup.sh` script, manually overwrite them i.e by sourcing another script overwriting the defaults.

### Commands:
##### rc_start_refbox
start the refbox and the vue frontend. the ui can then be accessed via: [http://localhost/](http://localhost/)

Env variables for configuration: 
- `REFBOX_IMAGE` image to use for refbox
- `REFBOX_TAG` tag to use for refbox
- `REFBOX_FRONTEND_IMAGE` image to use for refbox frontend
- `REFBOX_FRONTEND_TAG` tag to use for refbox frontend
- `REFBOX_CONFIG_GAME` game config to use in the refbox.
- `REFBOX_CONFIG_SIMULATION` simulation config to use in the refbox.
- `REFBOX_CONFIG_COMM` communication config to use in the refbox.
- `REFBOX_CONFIG_MPS` mps config to use in the refbox.
- `REFBOX_CONFIG_TEAM` team config to use in the refbox.

##### rc_start_simulator
start the rcll-simulator and the frontend for it. The ui can then be accessed via [http://localhost:4200/](http://localhost:4200/)``. 

Env variables for configuration: 
- `SIMULATOR_IMAGE` image to use for simulator
- `SIMULATOR_TAG` tag to use for simulator
- `SIMULATOR_FRONTEND_IMAGE` image to use for simulator frontend
- `SIMULATOR_FRONTEND_TAG` tag to use for simulator frontend
- `SIMULATOR_CONFIG_FILE` the config file used for the simulator.
