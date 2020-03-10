# -*- coding: utf-8 -*
import rospy
from zr_protocol.msg import led8_data8
from zr_protocol.msg import bit8_data
from zr_protocol.srv import hw_cmd
import time

def btns_callback_bit8_data(data):   
    rospy.loginfo(rospy.get_caller_id() + "btns event= '%s'", data.data)

def startnode_pc():    
    rospy.init_node('ledkey_pc', anonymous=True)
    #publish led8 、leds
    led8pub = rospy.Publisher('led8_data8', led8_data8, queue_size=1)
    ledspub = rospy.Publisher('leds_bit8_data', bit8_data, queue_size=1)
    #subscribe btns
    rospy.Subscriber("btns_bit8_data", bit8_data, btns_callback_bit8_data)
 
    if not rospy.has_param("~rate_param"):
        rospy.loginfo("no rate param be setted. default is 1")
    rvalue = rospy.get_param("~rate_param",1)
    

    rate = rospy.Rate(rvalue) # hz
    rospy.loginfo("zzz ledkey_pc node initok.")

    msg_led8=led8_data8()
    msg_leds=bit8_data()

    srv_name='zr_hw_cmd'
    rospy.wait_for_service(srv_name)
    #---------------------------service cmd--------------
    
    def runsrvcmd(cmd,data):
        rospy.loginfo("client:request '%s'."%cmd)             
        try:
            val = rospy.ServiceProxy(srv_name, hw_cmd)
            resp1 = val(cmd,data)
            rospy.loginfo ("client:response length=%s output='%s'"%(len(resp1.output),resp1.output))
        except rospy.ServiceException, e:
            rospy.loginfo ("err:%s"%e)
    
    #cmd:n,v,b,c,l>,l< ,b>,b<,lit(),chr()
    #---------------------------service cmd--------------nvbc
    rospy.loginfo("#-------test service cmd:n,v,b,c")
    reqlist=["n","v","b","c"]
    reqlen=len(reqlist)
    i=0
    while not rospy.is_shutdown():        
        i=i%reqlen
        runsrvcmd(reqlist[i],[])        
        i=i+1
        if(i==reqlen):
            break
        rate.sleep()

    #---------------------------service cmd--------------l<
    rospy.loginfo("#-------test service cmd:l<, please look at the high bit and low bit of the the leds.")
    runsrvcmd("l<",[]) 
    i=0
    while not rospy.is_shutdown():
        msg_leds.data=i
        ledspub.publish(msg_leds)
        time.sleep(0.05)
        i=i+1
        if(i==0xff):
            break
    #---------------------------service cmd--------------l>
    rospy.loginfo("#-------test service cmd:l>, please look at the high bit and low bit of the the leds.")
    runsrvcmd("l>",[]) 
    i=0
    while not rospy.is_shutdown():
        msg_leds.data=i
        ledspub.publish(msg_leds)
        time.sleep(0.05)
        i=i+1
        if(i==0xff):
            break
    #---------------------------service cmd--------------b<
    rospy.loginfo("#-------test service cmd:b<, please press buttons,and look the keyvalue.")
    runsrvcmd("b<",[]) 
    i=0
    while not rospy.is_shutdown():        
        rate.sleep()
        i=i+1
        if(i==10):
            break
    #---------------------------service cmd--------------b>
    rospy.loginfo("#-------test service cmd:b>, please press buttons,and look the keyvalue.")
    runsrvcmd("b>",[]) 
    i=0
    while not rospy.is_shutdown():        
        rate.sleep()
        i=i+1
        if(i==10):
            break
    #---------------------------service cmd--------------lit ()
    rospy.loginfo("#-------test service cmd:lit, led's lightness will be changed.")
    reqlist=["lit","lit","lit","lit","lit","lit","lit","lit","lit","lit"]
    reqdata=[(7,),(0,),(5,),(0,),(3,),(0,),(2,),(4,),(6,),(1,)]
    reqlen=len(reqlist)
    i=0
    while not rospy.is_shutdown():
        i=i%reqlen
        runsrvcmd(reqlist[i],reqdata[i])        
        i=i+1
        if(i>=reqlen):
            break
        rate.sleep()
    #---------------------------service cmd--------------chr ()
    rospy.loginfo("#-------test service cmd:chr, set 30 charaters data in to hardware.")
    chars=(0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71,0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71)
    runsrvcmd("chr",chars) 
    '''
    //数码管字形
    //  -     8
    // | |   3 7
    //  -     2
    // | |   4 6
    //  - .   5  1
    
    0B00111111,/*0*/ 0x3f
    0B00000110,/*1*/ 0x06
    0B01011011,/*2*/ 0x5B
    0B01001111,/*3*/ 0x4F

    0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71

    自定字形举例
    '|-'
    0B01110000  0x70
    '-|'
    0B01000110  0x46
    '''
    rospy.loginfo("#-------test service cmd:chr, set 2 charactors |- and -|,show they run.")
    runsrvcmd("chr",(0x70,0x46))# set '|-'、'-|' 
    
    #fly to right
    i=0
    while not rospy.is_shutdown():
        msg_led8.input=" "*i +"\x01"
        led8pub.publish(msg_led8)
        time.sleep(0.3)
        i=i+1
        if(i==7):
            break
    #fly to left
    i=0
    while not rospy.is_shutdown():
        msg_led8.input=" "*(7-i) +"\x02"
        led8pub.publish(msg_led8)
        time.sleep(0.3)
        i=i+1
        if(i==7):
            break
    rospy.loginfo("#-------test publish msg: led8_data8 and bit8_data,30hz.")
    #30hz publish msg
    rate = rospy.Rate(30) # hz
    a=10
    i=0
    while not rospy.is_shutdown():
        #---------------------------msg--------------
        a=a+1        
        hello_str = "out.%s" %(a)
        #rospy.loginfo(hello_str)   

        msg_led8.input=hello_str  
        led8pub.publish(msg_led8)

        msg_leds.data=a%0x100;
        ledspub.publish(msg_leds)

        i=i+1
        rate.sleep()

if __name__ == '__main__':
    try:
        startnode_pc()
    except rospy.ROSInterruptException:
        pass