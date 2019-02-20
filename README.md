## Scripts and documentation for hosting IoT and Microservices class at NYU CUSP

The repo contains two directories, [`IoT`](./IoT) and [`server`]('./server').

> As Phil Karlton said -- There are only two hard things in Computer Science: cache invalidation and naming things

Anyways, the `IoT` directory contains:

- Helper Scripts: for prepping, flashing and ad-hoc monitoring the Pi
  - `create_config.py` -- Prepping the Raspberry Pi (using [`raspberrypi-ua-netinst`](https://github.com/FooDeas/raspberrypi-ua-netinst) ) with dynamically generated ssh keys, IP addresses (more on this a little later).
  - `flash_image.py` Copying the required setup (netinst files from setup sub directory) and configuration files to the plugged-in micro sd-cards.
  - Monitoring scripts -- simple ssh and ping tests to make sure that when powered on, the Pi's are connected to the access point as passed into the (configuration file when prepping the Pi).

- presentation: This directory contains scripts and documents that are created in the class.
  - cheat_sheets -- some markdown files with handy linux commands
  - codes -- different scripts and python modules for performing sensing and uploading data to the server.
  - plots -- some intermediate plots generated for the presentation

- setup: Containing setup files for [`ua-netinst`](https://github.com/FooDeas/raspberrypi-ua-netinst)
  - raspberrypi-ua-netinst-v1.5.1 -- v1.5.1 of installer (support until Pi 2B)
  - raspberrypi-ua-netinst-v2.3.0 -- v2.3.0 of installer (support until Pi 3B+)


The `server` directory contains scripts and modules for serving the ssh and vpn keys to students for interacting with the Pis and a dashboard for visualizing the uploaded data.


More information can be found in [`IoT`](./IoT) and [`server`](./server) directories.
