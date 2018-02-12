import time
import HTU21DF

while True:
    print("Sending reset....")
    HTU21DF.htu_reset
    temperature = HTU21DF.read_temperature()
    print("The temperatur is %f C" % temperature)
