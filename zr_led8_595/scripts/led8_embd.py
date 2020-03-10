# -*- coding: utf-8 -*
import rospy
from std_msgs.msg import String
from zr_protocol.msg import led8_data8
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
    
    rospy.loginfo(rospy.get_caller_id() + "Led8 screen is diplay '%s'", data.input)

def sub():
    rospy.init_node('led8_embd', anonymous=True)
    #subscribe 8led8 display
    rospy.Subscriber("led8_data8", led8_data8, callback)
    #service server ,screen light,set chr ,set leds and btns sort.
    rospy.Service('zr_hw_cmd', hw_cmd, fun1)
    rospy.spin() 


if __name__ == '__main__':
    try:
        
        sub()
    except rospy.ROSInterruptException:
        pass