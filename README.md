Back in 2016, I ordered a number of wireless temperature sensors and a single USB device to listen for their messages from a company called Wireless Things out of Nottingham, UK. Their devices were great, but the company went under. Their software is published [here](https://github.com/WirelessThings). To simplify the deployment, I decided to share here how I've gotten it to work as a Docker container.

### Components

#### srf-stick-receiver
What I have called the srf-stick-receiver is in the original software called the MessageBridge, part of the LaunchPad. All of MessageBridge has been copied into this repository, and is as of early 2020 unchanged from the original repository. I've externalized the configuration file, so you can edit this even after building the image. Log files are also externalized.

#### mqtt-publisher
A more developed version of [simpleUDPListen.py](https://github.com/WirelessThings/WirelessThings-LaunchPad/blob/master/Examples/Python%20CLI/simpleUDPListen.py) from the original software is included. Read and edit the settings to suit your environment. At this point the configuration is not externalized and so baked into the image you build below.

### Installation

Edit the `MessageBridge.cfg` file to have the right setting for your serial port. For me, this is `/dev/ttyACM0`. If this is a different port for you, make sure to edit the `docker run` command listed below to have the same device mapped to inside the container.

In the `srf-stick-receiver` directory, run
```
docker build . -t "srf-stick-receiver"
```

And in the `mqtt-publisher` directory, run
```
docker build . -t "mqtt-publisher"
```

Then, start the `mqtt-publisher` component
```
docker run  -d -it \
            --name mqtt-publisher \
            -p 50140:50140/udp \
            mqtt-publisher
```
and the `srf-stick-receiver` component
```
docker run -d -it \
           --name srf-stick-receiver \
           --device /dev/ttyACM0:/dev/ttyACM0 \
           -v /usr/share/srf-stick-receiver/config:/config \
           -v /usr/share/srf-stick-receiver/logs:/logs \
           srd-bridge 
```

Please note that upon it's first start, `stf-stick-receiver` will die with the following message
```
2020-05-05 07:02:26,535 - Message Bridge - CRITICAL - No Config Loaded, Exiting
2020-05-05 07:02:26,552 - Message Bridge - CRITICAL - DIE
```
If you start it a second time (or if it is started a second time), it will have written a template configuration file into `/config` and should then work. If not, feel free to open the file to adjust settings as they should be. 

The serial port for my device is `/dev/ttyACM0` and I assume this will be the same for you. If not, change to the appropriate port in the above command and run. Do not forget to edit the configuration file accordingly. 

### License

This work is licensed under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).
