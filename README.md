# private12306
一个简单轻便的12306购票软件，代码少bug少，模块独立容易拓展

安装：

  1.命令：git clone git@github.com:hellfire1991/private12306.git
  
  2.进入项目目录：private12306
  
  3.命令：pip install virtualenv
  
  4.命令：virtualenv  env
    
  5.linux 进入 env/bin 目录后 命令： source activate        激活虚拟环境
  
    windows 进入 env/Script 文件夹后 命令 ：source activate        激活虚拟环境

  6.返回 private12306目录

  7.命令：pip install -r requirements.txt

    windows用户：pip install -r winrequirements.txt
  
  8.安装chrome浏览器，并安装selenium chrome驱动，网上教程很多，请自行百度
  
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

注意：由于tensorflow 和 keres的兼容问题，程序会报警告，但不影响使用，如果觉得碍眼，适当降低他们的版本

简介：

在阅读了12306以及py12306两个项目后根据自身需求写了一个比较简洁的程序（功能简单，代码容易读，bug也少）。感谢各位老大哥，读代码学到很多

比较适合对python有一定了解，并且仅用来满足个人和朋友购票需求的同学

使用request_html进行查询，selenium 登陆买票,减少12306网站修改cookie、url等一些操作带来的程序更新压力

支持多用户，并且每个用户可以设置多个购票需求，支持多线程

支持本地打码，打码成功率基本在100%，自己测试从没失败过>-<，（打码这段代码是完完全全抄easy12306的，尴尬脸）

长期更新优化，欢迎指正

交流群

916475351

  
  
