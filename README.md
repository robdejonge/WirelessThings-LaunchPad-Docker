Back in 2016, I ordered a number of wireless temperature sensors and a single USB device to listen for their messages from a company called Wireless Things out of Nottingham, UK. Their devices were great, but the company went under. Their software is published [here](https://github.com/WirelessThings). To simplify the deployment, I decided to share here how I've gotten it to work as a Docker container.

### Components

#### srd-bridge
What I have called the srd-bridge is in the original software called the MessageBridge, part of the LaunchPad. All of MessageBridge has been copied into this repository, and is as of early 2020 unchanged from the original repository. I've externalized the configuration file, so you can edit this even after building the image. Log files are also externalized.

#### llap-mqtt-bridge
A more developed version of [simpleUDPListen.py][https://github.com/WirelessThings/WirelessThings-LaunchPad/blob/master/Examples/Python%20CLI/simpleUDPListen.py] from the original software is included. Read and edit the settings to suit your environment. At this point the configuration is not externalized and so baked into the image you build below.

### Installation

Edit the `MessageBridge.cfg` file to have the right setting for your serial port. For me, this is `/dev/ttyACM0`. If this is a different port for you, make sure to edit the `docker run` command listed below to have the same device mapped to inside the container.

In both directories, run
```
docker build .
```

Then, run
```
docker run --name srd-bridge --device /dev/ttyACM0:/dev/ttyACM0 -v /usr/share/srd-bridge/config:/config -v /usr/share/srd-bridge/logs:/logs  -d -it srd-bridge

docker run --name llap-mqtt-bridge -p 50140:50140/udp  -d -it llap-mqtt-bridge
```

### License

This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).
