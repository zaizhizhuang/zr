import rospy
from zr_protocol.msg import led8_data8

def pub():
    a=10000
    rospy.init_node('led8_pub', anonymous=True)
    pub = rospy.Publisher('led8_data8', led8_data8, queue_size=10)

   
 
    if not rospy.has_param("~rate_param"):
        print("no rate param be setted. default is 3")
    rvalue = rospy.get_param("~rate_param",3)
    

    rate = rospy.Rate(rvalue) # 10hz
    rospy.loginfo("zzz led8_pub node initok.")

    msg=led8_data8()

    while not rospy.is_shutdown():
        a=a+1
        #hello_str = "hello world %s" % rospy.get_time()
        hello_str = "%s" %a
        rospy.loginfo(hello_str)   

        msg.input=hello_str  
        pub.publish(msg)
        
        rate.sleep()

if __name__ == '__main__':
    try:
        pub()
    except rospy.ROSInterruptException:
        pass