from config import PATH
import os,time

#日志输入
def log_input(user_name,text):
    print(time.ctime())
    print(user_name+":\n"+text)
    path=PATH.get("log_path")+user_name+".txt"
    with open(path,"a+")as f:
        f.write(time.ctime())
        f.write("\n")
        f.write(text)
        f.write("\n\n")
        f.flush()
        f.close()



