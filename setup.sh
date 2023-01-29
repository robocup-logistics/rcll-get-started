rcll_get_started_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export REFBOX_TAG=refactored
export REFBOX_FRONTEND_TAG=v1
export SIMULATOR_TAG=v1
export SIMULATOR_FRONTEND_TAG=v1


export REFBOX_IMAGE=quay.io/robocup-logistics/rcll-refbox
export REFBOX_FRONTEND_IMAGE=quay.io/robocup-logistics/rcll-sim-frontend
export SIMULATOR_IMAGE=quay.io/robocup-logistics/rcll-simulator
export SIMULATOR_FRONTEND_IMAGE=quay.io/robocup-logistics/rcll-simulator-frontend

export SIMULATOR_CONFIG_FILE=./../config/simulator/config.yaml

function rc_start_refbox() {
  cd $rcll_get_started_dir/compose_files
  docker-compose -f refbox.yaml up
}

function rc_refbox_shell() {
  docker exec -it compose_files_refbox_1 llsf-refbox-shell
}

function rc_start_simulator() {
  cd $rcll_get_started_dir/compose_files
  docker-compose -f simulation.yaml up
}