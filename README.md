# Raspberry Pi-based data logger for FluxTeq sensors

The [FluxTeq COMPAQ DAQ](https://www.fluxteq.com/product-page/compaq-daq) has a standard USB interface that can be plugged into a Raspberry Pi. This can then be used as a data logger to store data locally on the Pi's microSD card, or upload to an InfluxDB database on a remote server. This repo contains scripts that allow a Raspberry Pi heat flux data logger to be set up.

![rpi_datalogger](https://github.com/AKstudios/fluxteq_heatflux_rpi/blob/main/pics/rpi_compaqdaq_usb.jpg)

---
## Prerequisites

Run the following commands to install the prerequisits for the scripts to work:
```
sudo apt-get install python-pip
sudo pip install pyserial
sudo pip install influxdb
sudo pip install pathlib
```

---
## Instructions

1. Set WiFi SSID and password in the `wpa_supplicant.conf` file. Place this file in the boot partition on the microSD card. Add an empty _ssh_ file as well to enable ssh server on the Pi.
2. Copy the RPi heatflux folder to _/home/pi_ folder on the Raspberry Pi. You can use [FileZilla](https://filezilla-project.org/) to SSH into the Pi, or use a Linux-based machine to access the home directory on the microSD card.
3. In the `readserial.py`, edit the number of heatflux sensors used, and input their sensitivities. This will be located in the calibration sheets that come with the sensors themselves.
4. If you're pushing data to the cloud, open the `datalogger.py` file, edit the server URL, influxDB's port, username, password and database name. Otherwise you can comment out the influx session code and the data will be stored locally on the Pi.
5. To make sure the scripts are always running and restart automatically when they crash for whatever reason, the `script_handler.sh` file can be set to run on boot. It keeps checking if the files are running and restarts them if they aren't. Run the following command:

```
sudo nano /etc/rc.local
```

On the second last line, type the following:

```
cd /home/pi/heatflux;./script_handler.sh &
```

This will ensure the `script_handler.sh` always runs on boot, which will monitor the other scripts.

6. Run the following command to give root permissions to `script_handler.sh`

```
sudo chmod +x /home/pi/heatflux/script_handler.sh
```

