zr_screen_1602

跳线控制背光显示
可变电阻调节字符清晰度

硬件节点
rospy.Subscriber("screen_1602", screen_1602, callback)
rospy.Service('zr_hw_cmd', hw_cmd, fun1)

ros节点
pub = rospy.Publisher('screen_1602', screen_1602, queue_size=1) 
srv_name='zr_hw_cmd'
rospy.wait_for_service(srv_name)
/*----------------------------------------------------------------------*/
screen_1602.msg
string line1
string line2

分两行显示，每行16个字符

支持数字，英文，日文，一些特殊符号。
LCD1602内含有八个自定义的字符空间,
可通过service自定义符号到位置 1、2、3、4……7
可以发送“\x01\x02\x03\x04...”的字串来显示
注意位置0的自定义符号不能被显示，因为“\0”在设备中是字符串结束标志,而我们通讯的消息类型是字符串string。

通讯刷新频率10hz
屏幕信息不改变可以不发送msg数据，或者发送空串。
""空字符串，保留本行不变化。如line1="";line2="xxx";第一行不变化。
非空字符串，显示完串的每个字符后，行末尾清空。

发送一个空格即可清除一行，不必发送16个空格。如line1=" ";line2="xxx";第一行清空

service 请求和显示msg一般情况下不要同时发送。因为硬件资源有限，容不下太多消息。
如果需要自定义字型，建议先用service完成自定义，再发送msg显示。

为了确保通讯实时性，硬件内部控制屏幕刷新，采用固定频率按行分次刷新的方案。
所以当通讯刷新速度很快时，视觉上能感受到屏幕两行刷新的时间差。（为正常现象）



/*----------------------------------------------------------------------*/
hw_cmd.srv
string cmd
uint8[] input
---
uint8[] output

cmd命令支持的字符串有:"n","v","b","c","chr"
n代表name
v代表version
b代表brand
c代表copyright


chr代表自定义字形集，可以定义7个字形，需要参数数组input，input[9]就是字形数据。
每次可以执行chr可设置一个字形
input[0] 为id
input[1-9]为字形数据



自定义字形数据如下（这里没有id）
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
每个字形5*8个点，点阵数据8行，每行是数组的一个字节
bell字形如下

00100
01110
01110
01110
11111
00000
00100
00000

请您知晓：
执行chr 设置自定义字符时，会有设置不成功的情况。硬件程序增加了适当的延时，所以使用 chr 时请注意。
猜测可能是因为硬件pcf8574模块+1602模块的本身特性，与arduino第三方库不太兼容的原因。
如有错误，请各位老师多多指正！

示例代码

roslaunch zr_screen_1602 screen_1602_demo.launch
roslaunch zr_screen_1602 screen_1602_display.launch
roslaunch zr_screen_1602 screen_1602_fake.launch