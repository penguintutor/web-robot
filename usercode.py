# RPi Web Robot - user programs
# see http://www.penguintutor.com/rubyrobot
# user-code.py
# Copyright Stewart Watkiss 2014


# This code is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.


global current_direction

def dance1():
    ''' Make the robot dance '''
    
    current_direction = (1,1)
    motor_change()
    time.sleep(0.5);
    current_direction = (0,0)
    motor_change()
    time.sleep(0.5);
    current_direction = (2,2)
    motor_change()
    time.sleep(0.5);
    current_direction = (0,0)
    motor_change()
    time.sleep(0.5);

