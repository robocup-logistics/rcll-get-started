# Officialy Machine Network Setup

The competition machines are connected in a wifi network set up through a
ubiquiti U6 LR.

It requires a unifi controller to setup, for which the instructions are outlined
below.

Note that this is only needed in case changes to the network are required,
it is not required to have the controller running at all time.

## Connecting the AP

The AP needs a router to connect to. The official router of the league is a ubiquiti EdgeRouter 12.
TODO: Describe EdgeRouter setup.

Make sure the POE cable used for the AP is at least CAT 5E compatible.

## Running Unifi Controller

The Unifi controller can be run via docker:

```bash
docker-compose -f docker-compose.yml up
```

It also starts a mongodb instance on port 27018 which is used to store all
sensitive information.

## First Startup and Pairing
The TC typically maintains an instance of the DB with all necessary configuration.

Nevertheless, here is how to set up everything from scratch:
1. Connect the AP and the host machine of the unify controller to the router.
2. Make sure both have IP addresses assigned in the same range and the host machine can ping the AP.
3. Hard reset ubiquiti AP by pressing and holding the reset button for a few seconds.
4. Run the unifi controller and connect to https://localhost:8443
5. Create a new Controller using the UI. Tip: do not create a unifi account, instead
   go to advanced settings when prompted to login to a unifi account, which lets you enter a local account instead.
6. Under unifi devices tab, you should see the AP and it's IP address.
7. SSH onto the AP as user ubnt and with password ubnt and run
```bash
set-inform http://<ip-address-of-console>:8080/inform
```
8. In the web UI, adopt the AP
9. In Settings tab, set up a 5 GHz network called `RefBox.NET` with password `dieirrenivans`.
10. In unifi devices tab you can configure the channels of the wifi network.

### Access devices after pairing
SSH access will be disabled per default after pairing!
If you want to connect via SSH you need to go to the unifi console and search in settings for "Device Authentification".
There you can enable ssh access and set username and password.

## Flash FirmwareA
If you need to upgrade the firmware of the AP, download it, scp it to the AP via (make sure to copy to tmp as `fwupdate.bin`):
```
scp -O BZ.MT7622_6.6.78+15404.240829.0158.bin ubnt@192.168.1.20:/tmp/fwupdate.bin
```
and then run via:
```
syswrapper.sh upgrade2 &
```
