from look_for_ticket.find_ticket import FIND_TICKET
from buy_ticket.buy_ticket import BUY_TICKET
from extension.log import log_input
from extension.check_before_start import CHECKER
import threading
import time
import random

#启动前检查用户输入参数是否正确

class APP(object):
    #全局变量储存栈
    checker=CHECKER
    local_stack=threading.local()
    def __init__(self,users,querys):
        self.users=users
        self.query=querys

    def get_mission(self):
        #获取符合要求的任务（票据信息）
        query=APP.local_stack.query
        self.finder = FIND_TICKET(query)
        time.sleep(1)
        while not APP.local_stack.mission:
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
        mission=APP.local_stack.mission.pop()
        res =self.buyer.buy_ticket(mission)
        return res

    @classmethod
    def start_mission(cls,user,query):
        app=cls(user,query)
        APP.local_stack.user=user
        APP.local_stack.query=query
        log_input(APP.local_stack.user["user_name"], "开始登陆")
        try:
            app.buyer=BUY_TICKET(user,query)
        except:
            raise EOFError("用户登陆失败，请检查账号密码是否正确")
        log_input(APP.local_stack.user["user_name"], "登陆成功，买手就位")
        APP.local_stack.mission = []
        while True:
            try:
                app.get_mission()
            except:
                log_input(APP.local_stack.user["user_name"], "查询失败")
                raise
            log_input(APP.local_stack.user["user_name"],"开始买票")
            res = app.execute_mission()
            if res == "succeeded":
                log_input(APP.local_stack.user["user_name"],"买票成功，请在30分钟内进入12306app付款")
                break
            else:
                pass

    @classmethod
    def start(cls,users,querys):
        CHECKER.check_before_start(users,querys)
        APP.users=users
        APP.querys=querys
        thread_list=[]
        if len(users)==1:
            user = users[0]
            query=querys.get(user['user_name'])
            log_input(user["user_name"], "*" * 120)
            log_input(user["user_name"], "程序启动")
            log_input(user["user_name"], "载入用户")
            cls.start_mission(user,query)
            return  None
        else:
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


