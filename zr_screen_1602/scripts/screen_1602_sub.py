import rospy
from std_msgs.msg import String
from zr_protocol.msg import screen_1602


def callback(data):   
    rospy.loginfo(rospy.get_caller_id() + " screen-1602 is diplay '%s' \\n %s"%(data.line1, data.line2))

def sub():
	rospy.init_node('screen_1602_sub', anonymous=True)
	rospy.Subscriber("screen_1602", screen_1602, callback)
	rospy.spin() 


if __name__ == '__main__':
    try:
        
        sub()
    except rospy.ROSInterruptException:
        pass