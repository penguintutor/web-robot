Install guide for web-robot
===========================

Copy the web-robot files to folder /home/pi/robot on the Raspberry Pi.

This can be done by using

wget https://github.com/penguintutor/web-robot/archive/master.zip 

unzip master.zip

mv web-remote-master robot


Copy the Bottle module into the /home/pi/robot directory.

Download Bottle from:
https://raw.githubusercontent.com/defnull/bottle/master/bottle.py


More information on bottle is available from:
http://bottlepy.org/docs/dev/index.html

Download jquery minimum file into the /home/pi/robot/public  directory:

wget http://code.jquery.com/jquery-2.1.3.min.js 

mv jquery-2.1.3.min.js /home/pi/robot/public/jquery.min.js

Set the command executable
sudo chmod 755 web-robot.py

Run the program using:
sudo ./web-robot.py

and then access through a browser to port 80 on the Raspberry Pi.

There is also an init script which should be copied to init.d and added to the startup scripts

sudo cp webrobot-init /etc/init.d/webrobot
sudo update-rc.d webrobot defaults


