zr_ledkey_1638
硬件节点的发布订阅
    #subscribe 8led8 display
    rospy.Subscriber("led8_data8", led8_data8, callback_led8_data8)
    #subscribe leds display
    rospy.Subscriber("leds_bit8_data", bit8_data, callback_bit8_data)
    #publish buttons event
    btns_pub = rospy.Publisher('btns_bit8_data', bit8_data, queue_size=1)
硬件节点的service server
    #service server ,screen light,set chr ,set leds and btns sort。
    rospy.Service('zr_hw_cmd', hw_cmd, fun1)



ros节点中订阅发布
    #publish led8 、leds
    led8pub = rospy.Publisher('led8_data8', led8_data8, queue_size=1)
    发布数码管显示的字串，最长16个字符。
    ledspub = rospy.Publisher('leds_bit8_data', bit8_data, queue_size=1)
    发布led灯显示的8bit数
    #subscribe btns
    rospy.Subscriber("btns_bit8_data", bit8_data, btns_callback_bit8_data)
    订阅按键事件，独立按键按下释放时会发布键值消息。可以通过消息判断按键情况。（支持多键触发）
ros节点中serviceclient
    srv_name='zr_hw_cmd'
    rospy.wait_for_service(srv_name)
    val = rospy.ServiceProxy(srv_name, hw_cmd)
    resp1 = val(reqlist[i],reqdata[i])

/*----------------------------------------------------------------------*/
led8_data8.msg 
string input

字串不计“.”号，最多8个字符，支持数字，英文字母
通讯刷新频率30hz
/*----------------------------------------------------------------------*/
bit8_data.msg 
uint8 data

8位无符号数据，
消息可用于控制8个led灯的点亮状态。
可以传递8个独立按键的状态。
等等


/*----------------------------------------------------------------------*/
hw_cmd.srv
string cmd
uint8[] input
---
uint8[] output

cmd命令支持的字符串有:"n","v","b","c","l>","l<" ,"b>","b<","lit","chr"
n代表name
v代表version
b代表brand
c代表copyright

l>代表LED排列高位在左，低位在右（默认）
l<代表LED排列高位在右，低位在左
b>代表BTN排列高位在左，低位在右（默认）
b<代表BTN排列高位在右，低位在左
lit代表light，控制数码管和LED的亮度 需要参数数组input，input[0]就是亮度值，取值范围0-7.
chr代表自定义字形集，可以定义30个字形，需要参数数组input，input[0-29]就是字形数据。

设置自定义字形原理

    '''
    //数码管字形
    //  -     8
    // | |   3 7
    //  -     2
    // | |   4 6
    //  - .   5  1

    位顺序：0B12345678
    
    0B00111111,/*0*/ 0x3f
    0B00000110,/*1*/ 0x06
    0B01011011,/*2*/ 0x5B
    0B01001111,/*3*/ 0x4F
    
    '''

根据规则，字形（0-10-A-F）如下所示
(0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71)
您可以根据需要定义自己的字形
    自定字形举例
    '|-'
    0B01110000  0x70
    '-|'
    0B01000110  0x46
使用chr命令将字形数组送入硬件缓存可以按数组顺序调用

led8pub 发送字符消息即可显示出配置的字符，1-30（注意编号从1开始）调用缓存数组[0-29]
'\x01\x02\x03\x04\x05\x06\x07\x08 \x09\x0a\x0b\x0c\x0d\x0e\x0f \x10\x11\x12\x13\x14\x15\x16\x17 \x18\x19\x1a\x1b\x1c\x1d\x1e'


硬件内置字符支持数字和英文字母，字形如下
static unsigned char numbers[]={
0B00111111,/*0*/
0B00000110,/*1*/
0B01011011,/*2*/
0B01001111,/*3*/
0B01100110,/*4*/
0B01101101,/*5*/
0B01111101,/*6*/
0B00100111,/*7*/
0B01111111,/*8*/
0B01101111/*9*/
};
static unsigned char characters[]={
0B01110111,/*A*/
0B01111100,/*B*/
0B00111001,/*C*/
0B01011110,/*D*/
0B01111001,/*E*/
0B01110001,/*F*/
0B00111101,/*G*/
0B01110110,/*H*/
0B00010001,/*I*/
0B00001110,/*J*/
0B01110010,/*K*/
0B00111000,/*L*/
0B01010101,/*M*/
0B01010100,/*N*/
0B01011100,/*O*/
0B01110011,/*P*/
0B01100111,/*Q*/
0B01010000,/*R*/
0B01100101,/*S*/
0B01111000,/*T*/
0B00111110,/*U*/
0B00011100,/*V*/
0B01101010,/*W*/
0B00011101,/*X*/
0B01101110,/*Y*/
0B01001001/*Z*/
};


可用于ros机器人调试的数据、状态的显示以及按键交互。

示例代码

 roslaunch zr_ledkey_1638 ledkey_fake.launch
 roslaunch zr_ledkey_1638 ledkey_demo.launch



