import rospy
from std_msgs.msg import String
from zr_protocol.msg import led8_data8


def callback(data):   
    rospy.loginfo(rospy.get_caller_id() + "Led8 screen is diplay '%s'", data.input)

def sub():
	rospy.init_node('led8_sub', anonymous=True)
	rospy.Subscriber("led8_data8", led8_data8, callback)
	rospy.spin() 


if __name__ == '__main__':
    try:
        
        sub()
    except rospy.ROSInterruptException:
        pass