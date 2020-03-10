包名zr_protocol 
定义公有的通信协议消息，有msg，srv
此包是arduino和ros公用的一个包，编译之后，把此包生成 arduinolib用的头文件，放到arduino的IDE的lib目录下。
使用简化名称，如 zr_p 能节省arduino硬件的内存。

相关
https://blog.csdn.net/qq_38288618/article/details/104082877
ROS与Arduino硬件之rosserial_arduino（win10）


最终选择修改arduino 的 ros 库将相关名称使用flash储存。舍弃简化名称方案。
