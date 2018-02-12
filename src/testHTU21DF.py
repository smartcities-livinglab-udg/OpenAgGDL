# A simple program to test the driver

import time
from libs.HTU21DF import HTU21D

while True:
    print HTU21D(1).read_temperature()
