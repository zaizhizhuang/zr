zr_led8_595
硬件节点
    #subscribe 8led8 display
    rospy.Subscriber("led8_data8", led8_data8, callback)
    #service server ,screen light,set chr ,set leds and btns sort.
    rospy.Service('zr_hw_cmd', hw_cmd, fun1)

ros节点
    led8pub = rospy.Publisher('led8_data8', led8_data8, queue_size=10)
        发布数码管显示的字串，最长16个字符。
    srv_name='zr_hw_cmd'
    rospy.wait_for_service(srv_name)
/*----------------------------------------------------------------------*/
led8_data8.msg 
string input

字串不计“.”号，最多8个字符，支持数字，英文字母
通讯刷新频率30hz

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

chr代表自定义字形集，可以定义30个字形，需要参数数组input，input[0-29]就是字形数据。

设置自定义字形原理

    '''
    //数码管字形
    //  -     8
    // | |   3 7
    //  -     2
    // | |   4 6
    //  - .   5  1

    位顺序：0B87654321

    0B00000011, B10011111, B00100101, B00001101, B10011001
    0           1          2          3          4
    0x03        0x9f       0x25       0x0d       0x99
    
    '''
根据规则，字形（0-10-A-Z）如下所示
    0x3,0x9f,0x25,0xd,0x99,0x49,0x41,0x1b,0x1,0x9,0x11,0xc1,0x63,0x85,0x61,0x71,0x43,0x91,0x77,0x8f,0xb1,0xe3,0x55,0xd5,0xc5,0x31,0x19,0xf5,0x59,0xe1,0x83,0xc7,0xa9,0x47,0x89,0x6d

您可以根据需要定义自己的字形
    '|-'
    0B11110001  0xf1
    '-|'
    0B10011101  0x9d

使用chr命令将字形数组送入硬件缓存可以按数组顺序调用

led8pub 发送字符消息即可显示出配置的字符，1-30（注意编号从1开始）调用缓存数组[0-29]
'\x01\x02\x03\x04\x05\x06\x07\x08 \x09\x0a\x0b\x0c\x0d\x0e\x0f \x10\x11\x12\x13\x14\x15\x16\x17 \x18\x19\x1a\x1b\x1c\x1d\x1e'




硬件内置字符支持数字和英文字母，字形如下
int numbers[10] = {0B00000011, B10011111, B00100101, B00001101, B10011001, B01001001, B01000001, B00011011, B00000001, B00001001  };
//             0         1          2        3         4        5          6         7         8         9
int characters[26] = {
  B00010001, B11000001, B01100011, B10000101,
  /*ABCD//*/
  B01100001, B01110001, B01000011, B10010001,
  /*EFGH//*/
  B01110111, B10001111, B10110001, B11100011,
  /*IJKL//*/
  B01010101, B11010101, B11000101, B00110001,
  /*MNOP//*/
  B00011001, B11110101, B01011001, B11100001,
  /*QRST//*/
  B10000011, B11000111, B10101001, B01000111, B10001001, B01101101
  /*UVWXYZ//*/
};


可用于ros机器人调试的数据、状态的显示。

示例代码

roslaunch zr_led8_595 led8_fake.launch
roslaunch zr_led8_595 led8_demo.launch

video
https://www.bilibili.com/video/av95249210
gitbub
https://github.com/zaizhizhuang/zr