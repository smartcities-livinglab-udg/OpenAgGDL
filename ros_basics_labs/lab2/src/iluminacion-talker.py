import rospy
from std_msgs.msg import String
#"""The smbus package contains the classes used for I2C 
#communication. At the top of the Python script add the line"""
import smbus

#"""Variables de configuracion"""
LIN_LUM_ADDR = 0x39 # Direccion para leer sensor de iluminacion 0
LIN_LUM_REG_CTRL_VALUE_L = 0x0C
LIN_LUM_REG_CTRL_VALUE_H = 0x0D
bus = smbus.SMBus(1)

#"""metodo para leer el registro del sensor"""
def read_lum_reg(register):
    L = bus.read_byte_data(LIN_LUM_REG_CTRL_VALUE_L, register)
    H = bus.read_byte_data(LIN_LUM_REG_CTRL_VALUE_H, register) 
    
    return  

def run():
    #Topico para comunicar mensajes
    pub = rospy.Publisher("light_sensor", String, queue_size=10)
    # nombre del nodo
    rospy.init_node("light-talker", anonymous=True)
    
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        response = read_lum_reg(LIN_LUM_REG_CTRL_VALUE_L)
        rospy.loginfo(response)
        pub.publish(response)
        rate.sleep()

    
if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass

    #rospy.spin()

#def timer_callback(event):
#    global imu_pub
#
#    # Read our acceleration values.
#    x_accel = get_x_accel()
#    y_accel = get_y_accel()
#    z_accel = get_z_accel()
#
#    # Stuff the acceleration values into an Imu message and send it out.
#    imu_msg = Imu()
#    imu_msg.header.stamp = rospy.Time.now()
#    imu_msg.linear_acceleration.x = x_accel
#    imu_msg.linear_acceleration.y = y_accel
#    imu_msg.linear_acceleration.z = z_accel
#    imu_pub.publish(imu_msg)#