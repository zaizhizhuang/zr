
import rospy
from zr_protocol.srv import hw_info

def fun1(req):
    print "server:recv '%s'"%(req.input)
    return "return fake %s"%(req.input)

def main():
    rospy.init_node('info_srv_server_node', anonymous = True)
    rospy.Service('zr_hw_info', hw_info, fun1)
    rospy.spin()

if __name__ == '__main__':
    main()
