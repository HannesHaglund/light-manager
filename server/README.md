Install LIRC

sudo apt install lirc

Install wiringpi

git clone git://git.drogon.net/wiringPi
cd wiringPi
./build

Install rcswitch-pi
git clone https://github.com/r10r/rcswitch-pi.git
cd rcswitch-pi

Modify rcswitch-pi/send.cpp, so that you can use ./send <system> <unit> <on/off> to change the state of your outlets.

You build it via:

make

Once you're done, copy the binary to /usr/bin

sudo cp send /usr/bin
