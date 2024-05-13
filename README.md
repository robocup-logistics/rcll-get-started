# rcll-get-started
This repository bundles the documentation and setup details around the software used in the RCLL.
### General information
Most of the software used in the RCLL can be found in the [github organization](https://github.com/robocup-logistics). 
The docker images for the RCLL get published to the [quay](https://quay.io/organization/robocup-logistics).
#### Rules for RCLL
The rulebook for the RCLL can be found [here](https://github.com/robocup-logistics/rcll-rulebook).
#### Libraries for RCLL
There are various libraries to make communication with the refbox easy, at the moment there is one for [Java](https://github.com/robocup-logistics/rcll-java) and one for [C++](https://github.com/fawkesrobotics/protobuf_comm). Here you can find an [example](https://github.com/lef98/rcll_refbox_comm_example) that is using the C++ lib. For Communication with the refbox there is a mqtt bridge available which can be found [here](https://github.com/robocup-logistics/rcll-mqtt-bridge).

### Installation of this Repo
##### Prerequisites
To use this repository you have to have `docker`, `docker-compose`, `screen` and `bash` installed. To make the commands available you have to source `setup.sh`, you can do this in our local
`~/.bashrc`

### Configuration
All the commands that are listened below can be configured via various env variables. To overwrite the defaults which are set in the `setup.sh` script, manually overwrite them in the file `local_setup.sh`. This file is ignored in git and will be created automatically once you source the `setup.sh` for the first time.

If you want to play a c0 productino challenge, one must add `export REFBOX_CONFIG_CHALLENGE=./../config/refbox/challenge_prod_c0.yaml` into his `local_setup.sh`.

### Main Commands:

The main commands are
 - rc_start
 - rc_stop
 - rc_pull



##### rc_start

start the refbox and the vue frontend. the ui can then be accessed via: [http://localhost:8080/](http://localhost:8080/)

Main environment variables for configuration:
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

In the directory `config/refbox` are some configurations which are used by default. You can find more [here](https://github.com/robocup-logistics/rcll-refbox/tree/master/cfg]) in the rcll-refbox repository.

The startup utilizes docker-compose to spin up services and then sets up a screen session where the logs can be followed.
The screen session is named `${RC_SCREEN_NAME}`, which defaults to `rcll`.
The existing tabs in that session are always closed before re-launching.

##### rc_stop
This stops all services.

##### rc_pull
This pulls the newest version of all docker images.

#### Other Commands

The RCLL offers also some additional tools. For each, there are 3 commands:
 - rc_start_<tool> - which launches the tool
 - rc_stop_<tool> - which stops the tool
 - rc_pull_<tool> - which updates the docker containers for that tool

There are also options for each tool to be launched in the main commands above.

##### refbox

Used to just start the refbox and it's frontend without any other tools.
See the `rc_start` section for configuration options.

Note that the startup also checks for the existance of a MongoDB un `RC_MONGODB_URI`.

##### mongodb

The refbox requires a running MongoDB instance (any version compatible with the mongocxx-driver of the refbox).
Per default, a new MongoDB 5.0 is started on startup. But it is also possible to use an existing instance. Note that the refbox needs to be configured separately to also use the instance.

Env variables for configuration:
- `RC_MONGODB_START` set to true if a mongodb instance should start with the main command, defaults to `true`
- `RC_MONGODB_HOST` hostname or ip address where the instance should run on, defaults to `localhost`
- `RC_MONGODB_PORT` port where the intance should run on, defaults to `27017`
- `RC_MONGODB_URI` Final URI, defaults to` mongodb://${RC_MONGODB_HOST}:${RC_MONGODB_PORT}`

##### mongodb_backend

The refbox logs games into a database, the frontend of the refbox can display that data.
In order to do so, a small backend is required that bridges between the database and the frontend.

Env variables for configuration:
- `RC_MONGODB_BACKEND_START` set to true if the mongodb backend should be started with the main command, defaults to `false`
- `RC_MONGODB_BACKEND_DB_NAME` name of the database to use, defaults to `rcll`, which is the default name of the database the refbox uses.

Note that the backend also utilizes the `RC_MONGODB_URI` variable from the mongodb component.

##### mqtt_bridge

Note: The image is only available via ghcr.io, so you have to login in order to be able to pull it!

Env variables for configuration:
- `RC_MQTT_START` set to true if mqtt bridge should start with the main command
- `RC_MQTT_BROKER` broker to connect to
- `RC_MQTT_REFBOX` ip of the refbox
- `RC_MQTT_TEAM` team name
- `RC_MQTT_KEY` crypto key for refbox communication


##### simulator
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
