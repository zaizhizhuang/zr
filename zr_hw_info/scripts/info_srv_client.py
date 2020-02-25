import rospy

from zr_protocol.srv import hw_info
import time

def main():
    rospy.init_node('info_srv_client_node',anonymous=False)
    srv_name='zr_hw_info'
    
    rospy.wait_for_service(srv_name)
    reqlist=["name","version","brand","copyright"]
    reqlen=len(reqlist)
    i=0
    while(1):
        i=i%reqlen
        print("client:request '%s'."%reqlist[i])
             
        try:
            val = rospy.ServiceProxy(srv_name, hw_info)
            resp1 = val(reqlist[i])
            print ("client:response '%s'"%resp1.output)
        except rospy.ServiceException, e:
            print ("err:%s"%e)
        time.sleep(2)

        i=i+1

if __name__ == "__main__":
    main()
