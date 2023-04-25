# rcll-get-started
This repository bundles the documentation and setup details around the software used in the RCLL.
### General information
Most of the software used in the RCLL can be found in the [github organization](https://github.com/robocup-logistics). 
The docker images for the RCLL get published to the [quay](https://quay.io/organization/robocup-logistics).
#### Rules for RCLL
The rulebook for the RCLL can be found [here](https://github.com/robocup-logistics/rcll-rulebook).
#### Libraries for RCLL
There are various libraries to make communication with the refbox easy, at the moment there is one for [Java](https://github.com/robocup-logistics/rcll-java) and one for [C++](https://github.com/fawkesrobotics/protobuf_comm). Here you can find an [example](https://github.com/lef98/rcll_refbox_comm_example) that is using the C++ lib.

### Installation of this Repo
##### Prerequisites
To use this repository you have to have `docker`, `docker-compose` and `bash` installed. To make the commands available you have to source `setup.sh`, you can do this in our local 
`~/.bashrc`

### Configuration
All the commands that are listened below can be configured via various env variables. To overwrite the defaults which are set in the `setup.sh` script, manually overwrite them in the file `local_setup.sh`. This file is ignored in git and will be created automatically once you source the `setup.sh` for the first time.

If you want to play a c0 productino challenge, one must add `export REFBOX_CONFIG_CHALLENGE=./../config/refbox/challenge_prod_c0.yaml` into his `local_setup.sh`.

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
- `REFBOX_CONFIG_CHALLENGE` challenges config to use in the refbox.
- `REFBOX_CONFIG_MONGODB` mongodb config to use in the refbox.
  
In the folder `config/refbox` are some configuraitons which are used by default. You can find more [here](https://github.com/robocup-logistics/rcll-refbox/tree/master/cfg]) in the rcll-refbox repository.

##### rc_start_simulator
start the rcll-simulator and the frontend for it. The ui can then be accessed via [http://localhost:4200/](http://localhost:4200/)``. 

Env variables for configuration: 
- `SIMULATOR_IMAGE` image to use for simulator
- `SIMULATOR_TAG` tag to use for simulator
- `SIMULATOR_FRONTEND_IMAGE` image to use for simulator frontend
- `SIMULATOR_FRONTEND_TAG` tag to use for simulator frontend
- `SIMULATOR_CONFIG_FILE` the config file used for the simulator.

### Documentation For RCLL

Generally it is good to take a look at the refbox [wiki](https://github.com/robocup-logistics/rcll-refbox/wiki), which contains a lot of information.

#### Communication
Each Team has to communicate with the [refbox](https://github.com/robocup-logistics/rcll-refbox). This is done via the [rcll-protobuf-msgs](https://github.com/robocup-logistics/rcll-protobuf-msgs). You can find a detailed documentation on them [here](https://pkohout.github.io/rcll-protobuf-msgs/). In the refbox repository is a wiki entry giving a good overview of the communication, see this [link](https://github.com/robocup-logistics/rcll-refbox/wiki/Communication-Protocol#messages-sent-from-the-refbox)