import rospy
from zr_protocol.srv import hw_cmd

import time
val=None
def main():
    global val
    rospy.init_node('pwm16_pca9685_client_node',anonymous=False)

   
    srv_name='zr_hw_cmd'
    rospy.wait_for_service(srv_name)
    #---------------------------service cmd--------------

    def runsrvcmd(cmd,data,outlog=1):
        global val
        if(outlog): rospy.loginfo("client:request '%s'."%cmd)             
        try:
            if val is None:
                val = rospy.ServiceProxy(srv_name, hw_cmd)
            resp1 = val(cmd,data)
            if(outlog): 
                rospy.loginfo ("client:response length=%s output="%(len(resp1.output)))
                input_dat=[]
                recv_dat=[]
                for i in resp1.output:
                    recv_dat.append(int(ord(i)))
                    input_dat.append(hex(ord(i)))
                #rospy.loginfo( input_dat)
                #rospy.loginfo( recv_dat)
                '''errlist=[]
                for i in range (len(resp1.output)):
                    if(i<len(data)):
                        if (recv_dat[i] !=data[i]):
                            rospy.loginfo("err %s:"%(i) )
                            rospy.loginfo("    %s:"%data[i] )
                            rospy.loginfo("    %s:"%recv_dat[i] )
                '''
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
    #---------------------------service cmd--------------en ()
    rospy.loginfo("#-------test service cmd:en")
    # board0 first data
    runsrvcmd("ps",(0B00000000,0,146,100,100,100,100,100,100,100,  146,100,100,100,100,100,100,146))
    # board1 first data
    runsrvcmd("ps",(0B00000001,0,146,100,100,100,100,100,100,100,  146,100,100,100,100,100,100,146))
    runsrvcmd("en",(1,))#START RUN NOW!!!
    time.sleep(2)
    


    #---------------------------service cmd--------------ps ()
    rospy.loginfo("#-------test service cmd:ps, 1 byte data.")
    '''
    dmin*2+16=103;  dmin=44
    dmax*2+16=512;  dmax=248
    '''
    # board0 port8 ~ board1 port7
    reqlist=[\
    (0B00000000,8,44,100,100,100,100,100,100,100,  248,100,100,100,100,100,100,146),\
    (0B00000000,8,100,100,100,100,100,100,100,100,  200,100,100,100,100,100,100,44),\
    (0B00000000,8,146,100,100,100,100,100,100,100,  146,100,100,100,100,100,100,146),\
    (0B00000000,8,200,100,100,100,100,100,100,100,  100,100,100,100,100,100,100,248),\
    (0B00000000,8,230,100,100,100,100,100,100,100,  80,100,100,100,100,100,100,248),\
    (0B00000000,8,248,100,100,100,100,100,100,100,  44,100,100,100,100,100,100,100)\
    ]
    i=0
    reqlen=len(reqlist)
    while not rospy.is_shutdown():
        i=i%reqlen
        runsrvcmd("en",(0,))
        time.sleep(0.1)
        runsrvcmd("ps",reqlist[i])        
        runsrvcmd("en",(1,))
        time.sleep(0.5) 
        i=i+1       
        if(i>=reqlen):
            runsrvcmd("en",(0,))
            break
    
    
    time.sleep(2)
    rospy.loginfo("#-------test service cmd:ps, 2 byte data.")
    '''
    dmin=103;
    dmax=512;
    '''
    # board1 port0 ~  port15
    reqlist=[\
    (0B01000001,0,103,200,200,200,200,200,200,200,  512,200,200,200,200,200,200,146),\
    (0B01000001,0,150,200,200,200,200,200,200,200,  430,200,200,200,200,200,200,103),\
    (0B01000001,0,200,200,200,200,200,200,200,200,  300,200,200,200,200,200,200,146),\
    (0B01000001,0,300,200,200,200,200,200,200,200,  200,200,200,200,200,200,200,512),\
    (0B01000001,0,430,200,200,200,200,200,200,200,  150,200,200,200,200,200,200,248),\
    (0B01000001,0,512,200,200,200,200,200,200,200,  103,200,200,200,200,200,200,200)\
    ]

    def to2bytedata(olist):
        nlist=[]
        for arr in olist:
            arrlen = len(arr) - 1
            narr=list(arr)
            while arrlen >= 2:
                v = narr[arrlen]
                p = (v >> 8) & 0xff
                narr[arrlen] = v % 0x100
                narr.insert(arrlen, p)
                arrlen=arrlen-1
            nlist.append(tuple(narr))
            #print(narr)
        return nlist

    # NOTICE: You must trans datas to 2 byte types array!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    reqlist=to2bytedata(reqlist)

    i=0
    reqlen=len(reqlist)

    while not rospy.is_shutdown():
        i=i%reqlen
        runsrvcmd("en",(0,))
        time.sleep(0.1)
        runsrvcmd("ps",reqlist[i])        
        runsrvcmd("en",(1,))
        time.sleep(0.5) 

        i=i+1       
        if(i>=reqlen):
            runsrvcmd("en",(0,))
            break
    
    
    
    rospy.loginfo("#-------test service cmd:ps, test create data.")
    runsrvcmd("en",(0,))
    time.sleep(2)

    
    def createTestData(TT,AAAAAA,PPPP,per,count=16):
        dlist=[]
        dlist.append((TT<<6)|(AAAAAA%0x40))
        dlist.append(PPPP% 0x10)
        v=0
        c=count
        if(TT):
            v=int(103+per*(512-103))
            while c>0:
                dlist.append((v >> 8)&0xff)#High bits
                dlist.append(v % 0x100)#Low bits
                c=c-1
        else:
            v=int(44 + per * (248-44))
            while c > 0:
                dlist.append(v&0xff)
                c = c - 1
        return tuple(dlist)
    #datalist=createTestData(1,1,0,0.0)
    '''
    hardware buff size is 300 .
    so ,
    the count of single byte data must NOT more than 256.
    the count of double byte data must NOT more than 128.
    if you have 16+ boards,you can run "ps" command many times.
    '''
    #256 sigle byte data, board0~board15
    rospy.loginfo("#-------test 256 sigle byte data, board0~board15")
    runsrvcmd("en",(1,),0)
    runsrvcmd("ps",createTestData(0,0,0,0.25,256),0)
    time.sleep(0.5)
    runsrvcmd("ps",createTestData(0,0,0,0.5,256),0)
    time.sleep(0.5)
    runsrvcmd("ps",createTestData(0,0,0,0.75,256),0)
    time.sleep(0.5)
    #128 double byte data, board0~board7
    rospy.loginfo("#-------test 128 double byte data, board0~board7 .")
    runsrvcmd("ps",createTestData(1,0,0,0.25,128),0)
    time.sleep(0.5)
    runsrvcmd("ps",createTestData(1,0,0,0.5,128),0)
    time.sleep(0.5)
    runsrvcmd("ps",createTestData(1,0,0,0.75,128),0)
    time.sleep(0.5)    
    runsrvcmd("en",(0,),0)
    time.sleep(2)

    rospy.loginfo("#-------test service cmd:sm,  smoth motion .")
    i=0
    spd=10
    sf=10
    a=spd
    
    rospy.loginfo("# motion smoth mode, start.")
    runsrvcmd("sm",(1,),0)
    runsrvcmd("en",(1,),0)
    tc=0
    while not rospy.is_shutdown():       
        #change position  
        i=i+a       
        if(i>=512):            
             #change spd 1~100
            spd=spd+sf
            if(spd>=100):
                sf=-10
                spd=100
            if(spd<=10):
                sf=10
                spd=10  

            i=511
            a=-spd
        if(i<=0):
            i=0
            a=spd
            rospy.loginfo("spd%s"%spd)
            if(spd==10):
                tc=tc+1

        per=(i%512)/512.0 #0.0~1.0
        #NOTICE:when smoth mode start, PPPP is always 0,only one board's 16 ports can be controlled ,exmp, AAAAAA=1
        runsrvcmd("ps",createTestData(0,1,0,per,16),0)#createTestData(TT,AAAAAA,PPPP,per,count=16)
        time.sleep(0.04) 
        
        if(tc==1):
            tc=2
            runsrvcmd("sm",(0,),0)
            rospy.loginfo("# motion smoth mode, stop.")
        if(tc==3):
            tc=0
            runsrvcmd("sm",(1,),0)
            rospy.loginfo("# motion smoth mode, start.")
            

    
    runsrvcmd("en",(0,))
   
    
    
if __name__ == '__main__':
    try:
        
        main()
    except rospy.ROSInterruptException:
        pass