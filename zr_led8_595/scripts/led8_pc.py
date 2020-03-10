# -*- coding: utf-8 -*
import rospy
from zr_protocol.msg import led8_data8
from zr_protocol.srv import hw_cmd
import time

def pub():
    
    rospy.init_node('led8_pub', anonymous=True)
    led8pub = rospy.Publisher('led8_data8', led8_data8, queue_size=10)

   
 
    if not rospy.has_param("~rate_param"):
        print("no rate param be setted. default is 3")
    rvalue = rospy.get_param("~rate_param",3)
    

    rate = rospy.Rate(rvalue) # 10hz
    rospy.loginfo("zzz led8_pub node initok.")

    msg_led8=led8_data8()

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
    
    #cmd:n,v,b,c,chr()
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

    #---------------------------service cmd--------------chr ()
    rospy.loginfo("#-------test service cmd:chr, set 30 charaters data in to hardware.")
    chars=(0x3,0x9f,0x25,0xd,0x99,0x49,0x41,0x1b,0x1,0x9,0x11,0xc1,0x63,0x85,0x61,0x71,0x43,0x91,0x77,0x8f,0xb1,0xe3,0x55,0xd5,0xc5,0x31,0x19,0xf5,0x59,0xe1,0x83,0xc7,0xa9,0x47,0x89,0x6d)
    runsrvcmd("chr",chars) 
    '''
    //数码管字形
    //  -     8
    // | |   3 7
    //  -     2
    // | |   4 6
    //  - .   5  1
    0B87654321

    0B00000011, B10011111, B00100101, B00001101, B10011001
    0           1          2          3          4
    0x03        0x9f       0x25       0x0d       0x99

    0x3,0x9f,0x25,0xd,0x99,0x49,0x41,0x1b,0x1,0x9,0x11,0xc1,0x63,0x85,0x61,0x71,0x43,0x91,0x77,0x8f,0xb1,0xe3,0x55,0xd5,0xc5,0x31,0x19,0xf5,0x59,0xe1,0x83,0xc7,0xa9,0x47,0x89,0x6d

    自定字形举例
    '|-'
    0B11110001  0xf1
    '-|'
    0B10011101  0x9d
    '''
    rospy.loginfo("#-------test service cmd:chr, set 2 charactors |- and -|,show they run.")
    runsrvcmd("chr",(0xf1,0x9d))# set '|-'、'-|' 
    time.sleep(3)
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
    
    a=10
    while not rospy.is_shutdown():
        a=a+1
        #hello_str = "hello world %s" % rospy.get_time()
        hello_str = "out.%s" %(a)
        #rospy.loginfo(hello_str)   

        msg_led8.input=hello_str  
        led8pub.publish(msg_led8)
        
        rate.sleep()

if __name__ == '__main__':
    try:
        pub()
    except rospy.ROSInterruptException:
        pass