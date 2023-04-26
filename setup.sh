rcll_get_started_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

export REFBOX_TAG=latest
export REFBOX_FRONTEND_TAG=latest
export SIMULATOR_TAG=v1
export SIMULATOR_FRONTEND_TAG=v1


export REFBOX_IMAGE=quay.io/robocup-logistics/rcll-refbox
export REFBOX_FRONTEND_IMAGE=quay.io/robocup-logistics/rcll-refbox-frontend
export SIMULATOR_IMAGE=quay.io/robocup-logistics/rcll-simulator
export SIMULATOR_FRONTEND_IMAGE=quay.io/robocup-logistics/rcll-simulator-frontend

export SIMULATOR_CONFIG_FILE=./../config/simulator/config.yaml
export REFBOX_CONFIG_GAME=./../config/refbox/game.yaml
export REFBOX_CONFIG_SIMULATION=./../config/refbox/simulation.yaml
export REFBOX_CONFIG_COMM=./../config/refbox/comm.yaml
export REFBOX_CONFIG_MPS=./../config/refbox/mps.yaml
export REFBOX_CONFIG_TEAM=./../config/refbox/team.yaml
export REFBOX_CONFIG_CHALLENGE=./../config/refbox/challenge_disabled.yaml
export REFBOX_CONFIG_MONGODB=./../config/refbox/mongodb.yaml
function rc_start_refbox() {
  cd $rcll_get_started_dir/compose_files
  docker-compose -f refbox.yaml up
}

function rc_start_simulator() {
  cd $rcll_get_started_dir/compose_files
  docker-compose -f simulation.yaml up
}

function rc_dump_game_reports() {
  date=$(date +"%Y-%m-%d_%T")
  command=$(echo mongodump -d rcll -c game_report --gzip --archive=/data/db/game_report_$date.gz)
  docker exec mongodb $command
  mv $rcll_get_started_dir/compose_files/data/game_report_$date.gz game_report_$date.gz
}

function rc_restore_game_reports() {
  date=$(date +"%Y-%m-%d_%T")
  cp $1 $rcll_get_started_dir/compose_files/data/TMP_$date.gz
  command=$(echo mongorestore --gzip --archive=/data/db/TMP_$date.gz)
  docker exec mongodb $command
  rm $rcll_get_started_dir/compose_files/data/TMP_$date.gz
}

function rc() {
 cd $rcll_get_started_dir
}

LOCAL_SETUP=$rcll_get_started_dir/local_setup.sh
if [ ! -f "$LOCAL_SETUP" ]; then
  echo "local settings [$LOCAL_SETUP] DOES NOT exist, creating empty file!"
  echo "" > $LOCAL_SETUP
fi

DATA_FOLDER=$rcll_get_started_dir/compose_files/data
if [ ! -d "$DATA_FOLDER" ]; then
  echo "data mount for mongodb [$DATA_FOLDER] DOES NOT exist, creating empty file!"
  mkdir -p $DATA_FOLDER
fi
source $LOCAL_SETUP

