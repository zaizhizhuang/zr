# -*- coding: utf-8 -*
import rospy
from std_msgs.msg import String
from zr_protocol.msg import led8_data8
from zr_protocol.msg import bit8_data
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
    elif(req.cmd=="l>"):
        pass
    elif(req.cmd=="b>"):
        pass
    elif(req.cmd=="l<"):
        pass
    elif(req.cmd=="b<"):
        pass
    elif(req.cmd=="chr"):
        pass
    elif(req.cmd=="lit"):
        pass
    
    
    return b"return fake %s %s"%(req.cmd,'=test data')

def callback_led8_data8(data):   
    rospy.loginfo(rospy.get_caller_id() + "Led8 screen is diplay '%s'", data.input)

def callback_bit8_data(data):   
    rospy.loginfo(rospy.get_caller_id() + "Leds is diplay '%s'", data.data)

def startnode_embd():
    rospy.init_node('ledkey_embd', anonymous=True)
    #subscribe 8led8 display
    rospy.Subscriber("led8_data8", led8_data8, callback_led8_data8)
    #subscribe leds display
    rospy.Subscriber("leds_bit8_data", bit8_data, callback_bit8_data)
    #publish buttons event
    btns_pub = rospy.Publisher('btns_bit8_data', bit8_data, queue_size=1)
    #service server ,screen light,set chr ,set leds and btns sort。
    rospy.Service('zr_hw_cmd', hw_cmd, fun1)

    if not rospy.has_param("~rate_param"):
        rospy.loginfo("no rate param be setted. default is 3")
    rvalue = rospy.get_param("~rate_param",3)
    

    rate = rospy.Rate(rvalue) # 10hz
    rospy.loginfo("zzz ledkye_embd node initok.")

    btns_msg=bit8_data()
    a=0
    while not rospy.is_shutdown():
        a=a+1
        a=a%0x100
        #hello_str = "%s" %a
        #rospy.loginfo(hello_str)   

        btns_msg.data=a 
        btns_pub.publish(btns_msg)
        
        rate.sleep()


if __name__ == '__main__':
    try:
        
        startnode_embd()
    except rospy.ROSInterruptException:
        pass