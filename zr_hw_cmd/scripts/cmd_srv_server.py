
import rospy
from zr_protocol.srv import hw_cmd

def fun1(req):
    print "server:recv cmd='%s' input.length=%s input=%s"%(req.cmd,len(req.input),req.input)
    return b"return fake %s %s"%(req.cmd,'=test data')

def main():
    rospy.init_node('cmd_srv_server_node', anonymous = True)
    rospy.Service('zr_hw_cmd', hw_cmd, fun1)
    rospy.spin()

if __name__ == '__main__':
    main()
