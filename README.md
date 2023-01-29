# rcll-get-started
This repository bundles the documentation and setup details around the software used in the RCLL.
### General information
Most of the software used in the RCLL can be found in the [github organization](https://github.com/robocup-logistics). The docker images for the RCLL get published to the [quay organization](https://quay.io/organization/robocup-logistics)
### Installation
##### Prerequisites
To use this repository you have to have `docker`, `docker-compose` and `bash` installed. To make the commands available you have to source `setup.sh`, you can do this in our local 
`~/.bashrc`

### Configuration
All the commands that are listened below can be configured via various env variables. To overwrite the defaults which are set in the `setup.sh` script, manually overwrite them i.e by sourcing another script overwriting the defaults.

### Commands:
##### rc_start_refbox
start the refbox and the vue frontend. the ui can then be accessed via: `http://localhost:8080/`

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


##### rc_refbox_shell
start the refbox_shell (old ui for refbox).

##### rc_start_simulator
start the rcll-simulator and the frontend for it. The ui can then be accessed via `http://localhost:4200/`. 

Env variables for configuration: 
- `SIMULATOR_IMAGE` image to use for simulator
- `SIMULATOR_TAG` tag to use for simulator
- `SIMULATOR_FRONTEND_IMAGE` image to use for simulator frontend
- `SIMULATOR_FRONTEND_TAG` tag to use for simulator frontend
- `SIMULATOR_CONFIG_FILE` the config file used for the simulator.
