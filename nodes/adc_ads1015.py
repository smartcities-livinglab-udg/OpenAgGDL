#!/usr/bin/env python
import rospy,time
# Import the ADS1x15 module.
import Adafruit_ADS1x15
from std_msgs.msg import Float64

# Create an ADS1015 ADC (12-bit) instance.
adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

def read_chanel(chanel):
    # Read the specified ADC channel using the previously set gain value.
    # Note you can also pass in an optional data_rate parameter that controls
    # the ADC conversion time (in samples/second). Each chip has a different
    # set of allowed data rate values, see datasheet Table 9 config register
    # DR bit values.
    #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
    # Each value will be a 12 or 16 bit signed integer value depending on the
    # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    return adc.read_adc(chanel, gain=GAIN)

def create_topics(chanels):
    topics = [0]*len(chanels)

    for i in range(len(chanels)):
        topics[i] = rospy.Publisher("{}/raw".format(chanels[i][1]), Float64, queue_size=10)

    return topics

def set_param(param_name, value):
    rospy.set_param(param_name, value)

if __name__ == '__main__':
    rospy.init_node("adc_ads1015")
    rate = rospy.get_param("~rate_hz", 1)
    r = rospy.Rate(rate)
    chanels = [] #[index_chanel, topic_chanel]
    base_parms = "/var_types/environment_variables/{}{}"

    # ADS1015 tiene 4 canales
    for i in range(4):
        # Si existe el parametro ax se agrega su indice y topico correspondiente al array de canales
        if rospy.get_param("~a{}".format(i), False): chanels.append([i, rospy.get_param("~a{}_topic".format(i), "a{}_topic".format(i))])

    topics = create_topics(chanels)

    while not rospy.is_shutdown():

        for x in range(len(chanels)):
            data = read_chanel(chanels[x][0])
            rospy.loginfo("{} : [{}]".format(chanels[x][1], data))
            
            if data is not None:
                topics[x].publish(data)
                set_param(base_parms.format(chanels[x][1], "/last_value"), data)
        
        r.sleep()