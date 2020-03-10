hw_info.srv 输入输出皆为string（版本>1.20.xx.xx的舍弃此srv）

string input
---
string output


hw_cmd.srv 输入增加 string cmd，作为标识， 输入输出改为数组，通讯更为灵活。(代替 hw_info.srv)

string cmd
uint8[] input
---
uint8[] output


