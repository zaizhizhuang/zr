import rospy
from std_msgs.msg import String
from zr_protocol.srv import hw_cmd

def fun1(req):
    input_len=len(req.input)
    rospy.loginfo( "server:recv cmd='%s' input.length=%s input="%(req.cmd,input_len))
    if input_len:
        input_dat=[]
        for i in req.input:
            input_dat.append(hex(ord(i)))
        rospy.loginfo( input_dat)
    
    if(req.cmd=="n"):        
        pass
    elif(req.cmd=="v"):
        pass
    elif(req.cmd=="b"):
        pass
    elif(req.cmd=="c"):
        pass
    elif(req.cmd=="ps"):
        pass
    elif(req.cmd=="en"):
        pass
    return b"return fake %s %s"%(req.cmd,'=test data')



def sub():
    rospy.init_node('pwm16_pca9685_sub', anonymous=True)
    rospy.Service('zr_hw_cmd', hw_cmd, fun1)
    rospy.spin() 


if __name__ == '__main__':
    try:
        
        sub()
    except rospy.ROSInterruptException:
        pass