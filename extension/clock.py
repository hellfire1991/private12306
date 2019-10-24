import  time
from extension.log import log_input
def CLOCK():
    #夜间12306网站停机，设置时间检测，让脚本在12306网站停机时进入睡眠
    local_time=time.localtime()
    local_hour=local_time.tm_hour
    local_min=local_time.tm_min
    if local_hour>22:
        if local_min==59:
            set_clock()
        elif local_hour==23:
            set_clock()
        else:
            pass
    else:
        pass

def set_clock():
    log_input("超过11点12306网站停止订票,程序休眠")
    log_input("****************************************"
              "*******                        *********"
              "*******         程序休眠中       *********"
              "*******                        *********"
              "****************************************")
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
    log_input("超过6点网站可以正常订票")