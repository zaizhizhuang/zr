import rospy
from zr_protocol.srv import hw_cmd
from zr_protocol.msg import screen_1602
import time

def main():
    rospy.init_node('cmd_srv_client_node',anonymous=False)

    a=10000    
    pub = rospy.Publisher('screen_1602', screen_1602, queue_size=1)   
    msg=screen_1602()




    
    srv_name='zr_hw_cmd'
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
    rospy.wait_for_service(srv_name)
    #posilist=[1,2,3,4,5,6,7]
    reqlist=[\
    (1,0x4, 0xe, 0xe, 0xe, 0x1f, 0x0, 0x4),\
    (2,0x2, 0x3, 0x2, 0xe, 0x1e, 0xc, 0x0),\
    (3,0x0, 0xe, 0x15, 0x17, 0x11, 0xe, 0x0),\
    (4,0x0, 0xa, 0x1f, 0x1f, 0xe, 0x4, 0x0),\
    (5,0x0, 0xc, 0x1d, 0xf, 0xf, 0x6, 0x0),\
    (6,0x0, 0x1, 0x3, 0x16, 0x1c, 0x8, 0x0),\
    (7,0x0, 0x1b, 0xe, 0x4, 0xe, 0x1b, 0x0),\
    (8,0x1, 0x1, 0x5, 0x9, 0x1f, 0x8, 0x4)\
    ]
    reqlen=len(reqlist)
    i=0
    val=None

    while not rospy.is_shutdown():
        i=i%reqlen
        print("client:request ",reqlist[i])
             
        try:
            if val is None:
                val = rospy.ServiceProxy(srv_name, hw_cmd)
            resp1 = val("chr",reqlist[i])
            print ("client:response length=%s output="%(len(resp1.output)))
            print resp1.output
        except rospy.ServiceException, e:
            print ("err:%s"%e)
            
        i=i+1



        a=a+1
        #hello_str = "hello world %s" % rospy.get_time()
        hello_str = "%s" %a
        rospy.loginfo(hello_str)   

        msg.line1="1.02345678=%s"%hello_str  
        msg.line2='2\32\1\2\3\4\5\6\789\10\11\12\13\14\15'#"2 %s"%hello_str 
        msg.line2="2\32\1\2\3\4\5\6\7 %s"%hello_str  
        pub.publish(msg)
        time.sleep(0.03)

if __name__ == '__main__':
    try:
        
        main()
    except rospy.ROSInterruptException:
        pass