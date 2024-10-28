if [ -z "$rcll_get_started_dir" ]; then
    export rcll_get_started_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
fi

if [ -z "$rcll_compose_files_dir" ]; then
    rcll_compose_files_dir="${rcll_get_started_dir}/compose_files"
fi

export REFBOX_LOGS_DIR=$rcll_get_started_dir/logs
export REFBOX_FRONTEND_TAG=latest
export REFBOX_TAG=latest
export MONGODB_BACKEND_TAG=latest
export MONGODB_TAG=7.0
export MQTT_BRIDGE_TAG=master
export MQTT_BROKER_TAG=latest
export SIMULATOR_TAG=latest
export SIMULATOR_FRONTEND_TAG=latest

export REFBOX_COMPOSE_COMMAND=docker-compose


export REFBOX_FRONTEND_IMAGE=quay.io/robocup-logistics/rcll-refbox-frontend
export REFBOX_IMAGE=quay.io/robocup-logistics/rcll-refbox
export MONGODB_BACKEND_IMAGE=quay.io/robocup-logistics/mongodb-backend
export MONGODB_IMAGE=docker.io/library/mongo
export MQTT_BRIDGE_IMAGE=ghcr.io/robocup-logistics/rcll-mqtt-bridge
export MQTT_BROKER_IMAGE=docker.io/library/eclipse-mosquitto
export SIMULATOR_FRONTEND_IMAGE=quay.io/robocup-logistics/rcll-simulator-frontend
export SIMULATOR_IMAGE=quay.io/robocup-logistics/rcll-simulator

export REFBOX_CONFIG=./../config/refbox
export REFBOX_ARGS=


export RC_AUTO_SETUP=true
export RC_AUTO_START=false
export RC_MONGODB_START=true
export RC_MQTT_START=false
export RC_PROTOBUF_REBROADCASTER_START=false
export RC_MONGODB_BACKEND_START=false
export RC_MQTT_BROKER_START=false
export RC_SIMULATOR_START=false

export RC_SCREEN_NAME=rcll

export RC_MONGODB_PORT=27017
export RC_MONGODB_HOST=localhost
export RC_MONGODB_URI=mongodb://${RC_MONGODB_HOST}:${RC_MONGODB_PORT}
export RC_MONGODB_BACKEND_DB_NAME=rcll

export RC_MQTT_BROKER=tcp://localhost:1883
export RC_MQTT_REFBOX=localhost
export RC_MQTT_TEAM=GRIPS
export RC_MQTT_KEY=randomkey

export MQTT_BROKER_CONFIG=${rcll_get_started_dir}/config/mosquitto

function rc_setup_screen() {
  if ! screen -list | grep -q "${RC_SCREEN_NAME}"; then
    # Create a new screen session
    screen -dmS ${RC_SCREEN_NAME}
    screen -S ${RC_SCREEN_NAME} -X hardstatus alwayslastline
    screen -S ${RC_SCREEN_NAME} -X altscreen on
    screen -S ${RC_SCREEN_NAME} -X hardstatus string "%{= ky}%-Lw%{=r}%20>%n %t%{= ky}%+Lw %{= ky}%-=| %{= kw}%M%d %c%{-} %{=r} ${USER}@%H "
    screen -S ${RC_SCREEN_NAME} -X vbell off
    screen -S ${RC_SCREEN_NAME} -X defscrollback 5000

  fi
}

function rc_clear_screen_tabs() {
    local tab_name=$1
    local screen_name=${RC_SCREEN_NAME}

    # Find out the window numbers of windows with the specified name
    echo $(screen -S rcll -Q windows)
    WINDOW_IDS=$(screen -S rcll -Q windows | awk -v tab_name="${tab_name}" '{ for (i=2; i<=NF; i++) if ($i == tab_name) print $(i-1) }')
    if [ -n "$WINDOW_IDS" ]; then
      echo "Removing old screen tabs for $1"
      # Loop through each window ID and send the kill command
      echo "$WINDOW_IDS" | while IFS= read -r WINDOW_ID; do
          echo "Killing screen tab ${WINDOW_ID}"
          screen -S "$screen_name" -p "$WINDOW_ID" -X kill
      done
    fi
}

function rc_add_to_screen() {
  rc_setup_screen
  rc_clear_screen_tabs $1
  echo "Setting up screen tab $1"
  screen -S ${RC_SCREEN_NAME} -X screen -t "$1" ${REFBOX_COMPOSE_COMMAND} -f ${rcll_compose_files_dir}/$1.yaml logs -f
}


# Define a list of function names
function_names=("refbox" "mongodb_backend" "mqtt_bridge" "mongodb" "simulator" "mqtt_broker" "protobuf_rebroadcaster")

# Loop through the list and define functions
for func_name in "${function_names[@]}"; do
    # Define the function
    eval "rc_start_$func_name() {
      echo 'Starting ${func_name}'
      \${REFBOX_COMPOSE_COMMAND} -f \${rcll_compose_files_dir}/${func_name}.yaml up -d
      # Check if the exit code variable is set
      if [ -n "\${exit_code}" ]; then
          # Check if the exit code is not equal to 0
          if [[ "\${exit_code}" -ne 0 ]]; then
              # Do something if the exit code is not 0
              echo "Error: The exit code is not 0"
          fi
      else
          # Handle the case when the exit code variable is not set
          echo "Exit code is not sett"
      fi
      rc_add_to_screen ${func_name}
    }"
    eval "rc_stop_$func_name() {
      echo 'Stopping ${func_name}'
      \${REFBOX_COMPOSE_COMMAND} -f \${rcll_compose_files_dir}/${func_name}.yaml down
      rc_clear_screen_tabs ${func_name}
    }"
    eval "rc_pull_$func_name() {
      echo 'Pulling ${func_name}'
      \${REFBOX_COMPOSE_COMMAND} -f \${rcll_compose_files_dir}/${func_name}.yaml pull
    }"
    eval "rc_enter_$func_name() {
      echo 'Entering ${func_name}'
      docker exec -it $func_name /bin/sh
    }"
done

function rc_stop() {
  for func_name in "${function_names[@]}"; do
      ${REFBOX_COMPOSE_COMMAND} -f ${rcll_compose_files_dir}/${func_name}.yaml stop
  done
}

function rc_pull() {
  for func_name in "${function_names[@]}"; do
      ${REFBOX_COMPOSE_COMMAND} -f ${rcll_compose_files_dir}/${func_name}.yaml pull
  done
}
function rc_start() {
  if [ "${RC_MQTT_BROKER_START}" = "true" ]; then
    rc_start_mqtt_broker
  fi
  if [ "${RC_MONGODB_START}" = "true" ]; then
    rc_start_mongodb
  fi
  echo "Check Mongodb Connectivity on ${RC_MONGODB_URI} and start Refbox"
  rc_start_refbox
  if [ "${RC_AUTO_SETUP}" = "true" ]; then
    if [[ ! -z "${RC_CYAN}" ]]; then
      echo "CYAN will be: $RC_CYAN"
      #REFBOX_ARGS=$(echo "$REFBOX_ARGS && rcll-refbox-instruct -cyan $RC_CYAN")
      cmd=$(echo "sleep 5 && docker exec refbox rcll-refbox-instruct -c $RC_CYAN")
      echo "Will run in screen: $cmd"
      screen -m -d bash -c "$cmd"
    fi
    if [[ ! -z "${RC_MAGENTA}" ]]; then
      echo "MAGENTA will be: $RC_MAGENTA"
      cmd=$(echo "sleep 5 && docker exec refbox rcll-refbox-instruct -m $RC_MAGENTA")
      echo "Will run in screen: $cmd"
      screen -m -d bash -c "$cmd"
    fi

    if [ "${RC_AUTO_START}" = "true" ]; then
      echo "Autostart is activated!"
      cmd=$(echo "sleep 6 && docker exec refbox rcll-refbox-instruct -p SETUP && docker exec refbox rcll-refbox-instruct -s RUNNING")
      echo "Will run in screen: $cmd"
      screen -m -d bash -c "$cmd"
    fi
  fi
  if [ "${RC_SIMULATOR_START}" = "true" ]; then
    rc_start_simulator
  fi
  if [ "${RC_PROTOBUF_REBROADCASTER_START}" = "true" ]; then
    rc_start_protobuf_rebroadcaster
  fi
  if [ "${RC_MQTT_START}" = "true" ]; then
    rc_start_mqtt_bridge
  fi
  if [ "${RC_MONGODB_BACKEND_START}" = "true" ]; then
    rc_start_mongodb_backend
  fi
}

function rc_dump_game_reports() {
  date=$(date +"%Y-%m-%d_%T")
  command=$(echo mongodump -d rcll -c game_report --gzip --archive=/data/db/game_report_$date.gz)
  docker exec mongodb $command
}

function rc_restore_game_reports() {
  if [ -z "$1" ]; then
    echo "Please specify the archive to restore to the mongodb instance."
    return
  fi
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

export RC_MONGODB_DATA_DIR=$rcll_get_started_dir/compose_files/data
if [ ! -d "$RC_MONGODB_DATA_DIR" ]; then
  echo "data mount for mongodb [$RC_MONGODB_DATA_DIR] DOES NOT exist, creating empty file!"
  mkdir -p $RC_MONGODB_DATA_DIR
fi
source $LOCAL_SETUP
