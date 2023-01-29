rcll_get_started_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export REFBOX_TAG=refactored
export REFBOX_FRONTEND_TAG=v1

export REFBOX_IMAGE=quay.io/robocup-logistics/rcll-refbox
export REFBOX_FRONTEND_IMAGE=quay.io/robocup-logistics/rcll-sim-frontend
function rc_start_refbox() {
  cd $rcll_get_started_dir/compose_files
  docker-compose -f refbox.yaml up
}

function rc_refbox_shell() {
  docker exec -it compose_files_refbox_1 llsf-refbox-shell
}