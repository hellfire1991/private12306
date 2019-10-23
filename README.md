# pravite12306
一个简单轻便的12306购票软件，代码少bug少，模块独立容易拓展
安装：

  命令：git clone git@github.com:hellfire1991/pravite12306.git
  
  进入项目目录：pravite12306
  
  命令：pip install virtualenv
  
  命令：virtualenv  env
  
  命令：pip install -r requirements.txt
  
  安装chrome浏览器，并安装selenium chrome驱动，网上教程很多，请自行百度
  
使用：
  1.在main.py文件内按模板格式填写好账户信息和需要购买的车票信息
      USER_DATA=[{"user_name":"hello","password":"xxxxxxxx"},]

      #填写车票信息要注意严格按照模板填写，不然可能出现无法预测的bug
      QUERY_DATA={"hello":{
                                  #乘车日期(必填)
                                  "train_date":["2019-10-23",],

                                  #始发站2（必填）
                                  "from_station":"杭州",

                                  #到达站（必填）
                                  "to_station":"北京",

                                  #席别（土豪选填，不填就会有票就买，可能买到商务座，站票）
                                  "seats":["二等座",],

                                  #出发时间段（选填，可能半夜发车）
                                  "start_time_limit":[6,8],

                                  #到达时间段（选填）
                                  # "arrive_time_limit":[18,22],
                              },

      }

      if __name__=="__main__":

          APP.start(USER_DATA,QUERY_DATA)
      
      
  2.命令：python main.py
  
简介：
在阅读了12306以及py12306两个项目后根据自身需求写了一个比较简洁程序。感谢各位老大哥，读代码学到很多
比较适合对python有一定了解，并且仅用来满足个人和朋友购票需求的同学
支持多用户，并且每个用户可以设置多个购票需求，支持多线程
支持本地打码，打码成功率在基本在100%，自己测试从没没失败过>-<，（打码这段代码是完完全全抄easy12306的，尴尬脸）
长期更新优化，欢迎指正

交流群
916475351

  
  
