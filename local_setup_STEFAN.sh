#export REFBOX_CONFIG_CHALLENGE=./../config/refbox/challenge_nav.yaml
#export REFBOX_CONFIG_CHALLENGE=./../config/refbox/challenge_prod_c0.yaml
export REFBOX_CONFIG_CHALLENGE=./../config/refbox/challenge_disabled.yaml
export RC_CYAN=GRIPS
#export RC_MAGENTA=GRIPS
export REFBOX_IMAGE=registry.gitlab.com/grips_robocup/team_server/refbox
export REFBOX_FRONTEND_IMAGE=ghcr.io/pkohout/rcll-refbox-frontend
export REFBOX_FRONTEND_TAG=master
#export REFBOX_IMAGE=quay.io/robocup-logistics/rcll-refbox
#export REFBOX_TAG=refactored
export REFBOX_TAG=small_field
#export REFBOX_TAG=challenengefix
#export RC_AUTO_START=true
#export RC_MQTT_START=true
# rcll-refbox-instruct -m GRIPS
# rcll-refbox-instruct -p SETUP
# rcll-refbox-instruct -s RUNNING
# rcll-refbox-instruct -p PRODUCTION