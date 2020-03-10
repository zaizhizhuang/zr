import rospy
from zr_protocol.srv import hw_cmd
from zr_protocol.msg import screen_1602
import time
val=None
def main():
    global val
    rospy.init_node('cmd_srv_client_node',anonymous=False)

       
    pub = rospy.Publisher('screen_1602', screen_1602, queue_size=1)   
    msg=screen_1602()    
    srv_name='zr_hw_cmd'
    rospy.wait_for_service(srv_name)
    #---------------------------service cmd--------------

    def runsrvcmd(cmd,data):
        global val
        rospy.loginfo("client:request '%s'."%cmd)             
        try:
            if val is None:
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
        time.sleep(0.3)
    time.sleep(2)
    #---------------------------service cmd--------------chr ()
    rospy.loginfo("#-------test service cmd:chr, set 7 charaters data in to hardware.")
    '''
    //uint8_t bell[8]  = {0x4, 0xe, 0xe, 0xe, 0x1f, 0x0, 0x4};
    //uint8_t note[8]  = {0x2, 0x3, 0x2, 0xe, 0x1e, 0xc, 0x0};
    //uint8_t clock[8] = {0x0, 0xe, 0x15, 0x17, 0x11, 0xe, 0x0};
    //uint8_t heart[8] = {0x0, 0xa, 0x1f, 0x1f, 0xe, 0x4, 0x0};
    //uint8_t duck[8]  = {0x0, 0xc, 0x1d, 0xf, 0xf, 0x6, 0x0};
    //uint8_t check[8] = {0x0, 0x1, 0x3, 0x16, 0x1c, 0x8, 0x0};
    //uint8_t cross[8] = {0x0, 0x1b, 0xe, 0x4, 0xe, 0x1b, 0x0};
    //uint8_t retarrow[8] = {	0x1, 0x1, 0x5, 0x9, 0x1f, 0x8, 0x4};
    '''

    #posilist=[1,2,3,4,5,6,7]
    reqlist=[\
    (1,0x4, 0xe, 0xe, 0xe, 0x1f, 0x0, 0x4),\
    (2,0x2, 0x3, 0x2, 0xe, 0x1e, 0xc, 0x0),\
    (3,0x0, 0xe, 0x15, 0x17, 0x11, 0xe, 0x0),\
    (4,0x0, 0xa, 0x1f, 0x1f, 0xe, 0x4, 0x0),\
    (5,0x0, 0xc, 0x1d, 0xf, 0xf, 0x6, 0x0),\
    (6,0x0, 0x1, 0x3, 0x16, 0x1c, 0x8, 0x0),\
    (7,0x0, 0x1b, 0xe, 0x4, 0xe, 0x1b, 0x0),\
    (8,0x1, 0x1, 0x5, 0x9, 0x1f, 0x8, 0x4),\
    
    ]
    #8  is ok???why???
    reqlen=len(reqlist)
    i=0
    a=10000 
    

    while not rospy.is_shutdown():
        i=i%reqlen
        runsrvcmd("chr",reqlist[i]) 

        msg.line1="Srv cmd chr -->%s"%reqlist[i][0]
        msg.line2="\x01\x02\x03\x04\x05\x06\x07\x08\x09  %s"%reqlist[i][0] 
        pub.publish(msg)
        i=i+1
        
        time.sleep(2)
        if(i>=reqlen):
            break
    
    time.sleep(2)    
    
    rospy.loginfo("#-------test Show all chrs in LCD1602.")

    def getchrs(b,e):
        a =  range(b,e)
        for i in range(len(a)):
            a[i]=chr(a[i]%0x100)
        return "".join(a)

    i=1
    while not rospy.is_shutdown():
        msg.line1="Show chr %s-%s"%(i,i+15)
        msg.line2="%s"%getchrs(i,i+15) 
        pub.publish(msg)
        i=i+16
        if(i>0xff):
            i=1
            break
        time.sleep(1.5)
    time.sleep(2) 
    rospy.loginfo("#-------test clear line2, Show a counter after 2s. ")
    if not rospy.is_shutdown():
        msg.line1="Show Counter:"
        msg.line2=" " 
        pub.publish(msg)

    time.sleep(2)  
    a=10000 
    rospy.loginfo("#-------test the counter run at 20hz. ")
    while not rospy.is_shutdown():
        msg.line1=""#line1 no change
        msg.line2="\x01\x02\x03\x04\x05\x06\x07\x08\x09%s"%a
        pub.publish(msg)
        a=a+1        
        time.sleep(0.05)
if __name__ == '__main__':
    try:
        
        main()
    except rospy.ROSInterruptException:
        pass