import  time
from extension.log import log_input
class CLOCK(object):
    #夜间12306网站停机，设置时间检测，让脚本在12306网站停机时进入睡眠
    def __init__(self):
        pass
    @classmethod
    def check_clock(cls,user):
        local_time=time.localtime()
        local_hour=local_time.tm_hour
        local_min=local_time.tm_min
        if local_hour>22:
            if local_min==59:
                cls.set_clock(user)
            elif local_hour==23:
                cls.set_clock(user)
            else:
                pass
        elif local_hour<6:
            cls.set_clock(user)

    @classmethod
    def set_clock(cls,user):
        log_input(user,"23-6点12306网站停止订票,程序休眠")
        log_input(user,"****************************************\n"
                  "*******                        *********\n"
                  "*******         程序休眠中       *********\n"
                  "*******                        *********\n"
                  "****************************************\n")
        local_time = time.localtime()
        local_hour=local_time.tm_hour
        local_min=local_time.tm_min
        local_sec=local_time.tm_sec
        if local_hour>6:
            hour=24-int(local_hour)+6
        else:
            hour=6-int(local_hour)
        min=int(local_min)
        sec=int(local_sec)
        sleep_time=hour*3600-min*60-sec
        time.sleep(sleep_time)
        log_input(user,"超过6点网站可以正常订票")
if __name__=="__main__":
    pass