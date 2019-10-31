from look_for_ticket.find_ticket import FIND_TICKET
from buy_ticket.buy_ticket import BUY_TICKET
from extension.log import log_input
from extension.check_before_start import CHECKER
from extension.clock import CLOCK
import threading
import time
import random

#启动前检查用户输入参数是否正确

class APP(object):
    #程序启动前的参数检查器
    checker=CHECKER
    #程序休眠闹钟
    clock=CLOCK
    # 全局变量储存栈
    local_stack=threading.local()
    def __init__(self,users,querys):
        self.users=users
        self.query=querys
        self.finder=None
        self.buyer=None

    def get_mission(self):
        #获取符合要求的任务（票据信息）
        query=APP.local_stack.query
        self.finder = FIND_TICKET(query)
        time.sleep(1)
        while not APP.local_stack.mission:
            APP.clock()
            log_input(APP.local_stack.user["user_name"],"获取任务，开始查询")
            missions = self.finder()
            if missions:
                for mission in missions:
                    APP.local_stack.mission.append(mission)
                log_input(APP.local_stack.user["user_name"],"完成一次查询，发现符合要求的车票")
            else:
                log_input(APP.local_stack.user["user_name"],"完成一次查询，未发现符合要求的车票")
                time.sleep(random.randrange(5, 10))


    def execute_mission(self):
        #当查询器获取符合任务需求的票据信息时，进行买票操作
        mission=APP.local_stack.mission.pop()
        try:
            res =self.buyer.buy_ticket(mission)
        except:
            self.buyer.driver.close()
            raise Exception("买票失败，未知错误，请联系作者")
        return res

    @classmethod
    def start_mission(cls,user,query):
        app=cls(user,query)
        APP.local_stack.user=user
        APP.local_stack.query=query
        log_input(APP.local_stack.user["user_name"], "初始化浏览器")
        try:
            app.buyer=BUY_TICKET(user,query)
        except:
            raise Exception("浏览器初始化失败")
        log_input(APP.local_stack.user["user_name"], "浏览器初始化成功，买手就位")
        APP.local_stack.mission = []
        while True:
            try:
                app.get_mission()
            except:
                log_input(APP.local_stack.user["user_name"], "查询失败")
                raise Exception("查询失败")
            log_input(APP.local_stack.user["user_name"],"开始买票")
            res = app.execute_mission()
            if res == "succeeded":
                log_input(APP.local_stack.user["user_name"],"买票成功，请在30分钟内进入12306app付款")
                log_input(APP.local_stack.user["user_name"], "任务结束，退出线程")
                break
            else:
                app.buyer.driver.close()
                log_input(APP.local_stack.user["user_name"],"买票失败，再次尝试买票")
                log_input(APP.local_stack.user["user_name"], "重启浏览器")
                try:
                    app.buyer = BUY_TICKET(user, query)
                except:
                    raise Exception("浏览器初始化失败")
                log_input(APP.local_stack.user["user_name"], "浏览器初始化成功，买手就位")
                APP.local_stack.mission = []


    @classmethod
    def start(cls,users,querys):
        APP.checker.check_before_start(users,querys)
        APP.users=users
        APP.querys=querys
        if len(users)==1:
            user = users[0]
            query=querys.get(user['user_name'])
            log_input(user["user_name"], "*" * 120)
            log_input(user["user_name"], "程序启动")
            log_input(user["user_name"], "载入用户")
            cls.start_mission(user,query)
            return  None
        else:
            thread_list=[]
            for user in APP.users:
                log_input(user["user_name"], "*"*120)
                log_input(user["user_name"], "程序启动")
                log_input(user["user_name"], "载入用户，开启线程")
                query=querys.get(user["user_name"])
                t=threading.Thread(target=cls.start_mission,args=(user,query))
                t.start()
                thread_list.append(t)
                time.sleep(1)
            for t in thread_list:
                t.join()
            return  None


