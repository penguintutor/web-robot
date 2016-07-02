#Install guide for web-robot

This software is intended for install to a robot based on the Raspberry Pi Robot from PenguinTutor.com 

See [PenguinTutor.com Raspberry Pi Robot guide](http://www.penguintutor.com/electronics/rpirobot) 

It can also be used with the CamJam 3 robot


Copy the web-robot files to folder /home/pi/robot on the Raspberry Pi.

This can be done by using

```bash
wget https://github.com/penguintutor/web-robot/archive/master.zip 
unzip master.zip
mv web-remote-master robot
cd robot
```

Install Python Bottle

```bash
sudo apt-get install python3-bottle
```

Set the command so that it is executable
```bash
sudo chmod 755 web-robot.py
```

Run the program using:
```bash
sudo ./web-robot.py
```

and then access through a browser to port 80 on the Raspberry Pi.

There is also an init script which should be copied to init.d and added to the startup scripts

```bash
sudo cp webrobot-init /etc/init.d/webrobot
sudo update-rc.d webrobot defaults
```

## Configure the appropriate motor controller board

If using the controller design from the PenguinTutor robot guide, from the "Learn Electronics with Raspberry Pi" book or using the Ryantek controller board then no further configuration is required.

If using the CamJam EduKit 3 robotics kit then edit the file web-robot.py and change the line: 
```python
MOTORBOARD = 'penguintutor'
```
to:
```python
MOTORBOARD = 'camjam'
```