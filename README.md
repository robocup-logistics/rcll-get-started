# rcll-get-started
This repository bundles the documentation and setup details around the software used in the RCLL.
### General information
Most of the software used in the RCLL can be found in the [github organization](https://github.com/robocup-logistics). The docker images for the RCLL get published to the [quay organization](https://quay.io/organization/robocup-logistics)
### Installation
##### Prerequisites
To use this repository you have to have `docker`, `docker-compose` and `bash` installed. To make the commands available you have to source `setup.sh`, you can do this in our local 
`~/.bashrc`
### Commands:
##### rc_start_refbox
start the refbox and the vue frontend. the ui can then be accessed via: `http://localhost:8080/`

##### rc_refbox_shell
start the refbox_shell (old ui for refbox).
