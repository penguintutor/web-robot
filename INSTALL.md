Install guide for web-robot
===========================

This software is intended for install to a robot based on the Ruby Robot from PenguinTutor.com 

See [PenguinTutor.com Ruby Robot - Raspberry Pi robot guide](http://www.penguintutor.com/electronics/rubyrobot) 


Copy the web-robot files to folder /home/pi/robot on the Raspberry Pi.

This can be done by using

```bash
wget https://github.com/penguintutor/web-robot/archive/master.zip 
unzip master.zip
mv web-remote-master robot
```

Copy the Bottle module into the /home/pi/robot directory.
```bash
install Python Bottle
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

