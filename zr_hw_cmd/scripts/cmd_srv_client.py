import rospy

from zr_protocol.srv import hw_cmd
import time

def main():
    rospy.init_node('cmd_srv_client_node',anonymous=False)
    srv_name='zr_hw_cmd'
    
    rospy.wait_for_service(srv_name)
    reqlist=["name","version","brand","copyright","cmd1","cmd2"]
    reqlen=len(reqlist)
    i=0
    while(1):
        i=i%reqlen
        print("client:request '%s'."%reqlist[i])
             
        try:
            val = rospy.ServiceProxy(srv_name, hw_cmd)
            resp1 = val(reqlist[i],(65,int('0'),66,67,0xff,0x00))
            print ("client:response length=%s output='%s'"%(len(resp1.output),resp1.output))
        except rospy.ServiceException, e:
            print ("err:%s"%e)
        time.sleep(2)

        i=i+1

if __name__ == "__main__":
    main()
