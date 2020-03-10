import rospy
from std_msgs.msg import String
from zr_protocol.msg import screen_1602
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
    elif(req.cmd=="chr"):
        pass
    return b"return fake %s %s"%(req.cmd,'=test data')


def callback(data):   
    rospy.loginfo(rospy.get_caller_id() + " screen-1602 is diplay '%s' \\n %s"%(data.line1, data.line2))

def sub():
    rospy.init_node('screen_1602_sub', anonymous=True)
    rospy.Subscriber("screen_1602", screen_1602, callback)
    rospy.Service('zr_hw_cmd', hw_cmd, fun1)
    rospy.spin() 


if __name__ == '__main__':
    try:
        
        sub()
    except rospy.ROSInterruptException:
        pass