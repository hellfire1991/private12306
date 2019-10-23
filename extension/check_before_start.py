import re
from config import PATH
stations_path=PATH.get("stations_path")
import time
#检查参数

class CHECKER():

    stations_path=stations_path

    def __init__(self):
        pass

    @classmethod
    def check_before_start(cls,users,querys):
        for user in users:
            cls.check_user(user)
        for key,value in querys.items():
            cls.check_query(value)
    @classmethod
    def check_running_time(cls):
        pass


    @classmethod
    def check_user(cls,user):
        user_name=user["user_name"]
        if not user_name:
            raise ("请输入12306用户名")

        password=user["password"]
        if not password:
            raise ("请输入12306登陆密码")

    @classmethod
    def check_query(cls,query):
        #检查乘车日期
        train_dates=query.get("train_date")
        for data in train_dates:
            pattern1="^\d\d\d\d-[0-1]\d-[0-3]\d$"
            for date in train_dates:
                result=re.match(pattern1,date)
                if not result:
                    raise ("乘车日期格式填写错误")
        # 2019-10-20
        for train_date in train_dates:
            year,month,date=int(train_date[0:4]),int(train_date[5:7]),int(train_date[8:10])
            local_time=time.localtime()
            year_local,month_local,date_local=int(local_time.tm_year),int(local_time.tm_mon),int(local_time.tm_mday)
            if year>year_local:
                pass
            elif year_local==year:
                if month>month_local:
                    pass
                elif month==month_local:
                    if date>date_local or date==date_local:
                        pass
                    else:
                        raise ValueError("日期填写错误，车票日期应当大于或者等于当前日期")
                else:
                    raise ValueError("日期填写错误，车票日期应当大于或者等于当前日期")
            else:
                raise ValueError("日期填写错误，车票日期应当大于或者等于当前日期")

        #检查车站
        with open(stations_path,"r",encoding="utf-8") as f:
            stations_txt=str(f.readlines())
            from_station=query.get("from_station")
            pattern2="\\|"+from_station+"\\|"
            result=re.search(pattern2,stations_txt)
            if not result:
                raise ValueError("您填写的始发站不存在，请重新输入")

            to_station = query.get("to_station")
            pattern3 = "\\|"+to_station+"\\|"
            result = re.search(pattern3, stations_txt)
            if not result:
                raise ValueError("您填写的到达站不存在，请重新输入")

        #检查席别
        seat_type="|软卧|特等座|无座|硬卧|硬座|二等座|一等座|商务座|"
        seats=query.get("seats")
        for seat in seats:
            pattern4="\\|"+seat+"\\|"
            res=re.search(pattern4,seat_type)
            if not res:
                raise ValueError("您选择的席别不存在，请重新输入")

        #检查出发时间，到达时间
        if query.get("start_time_limit"):
            start_time=query.get("start_time_limit")
            if start_time[0] < 0 or start_time[1] > 24:
                raise ValueError("出发时间段应该限制在0-24之间")
        if  query.get("arrive_time_limit"):
            arrive_time=query.get("arrive_time_limit")
            if arrive_time[0]<0 or arrive_time[1]>24:
                raise ValueError("到达时间段应该限制在0-24之间")

if __name__ =="__main__":

    USER_DATA=[{"user_name":"hello","password":"xxxxxxx"},]

    QUERY_DATA={"hello":{
                                #乘车日期
                                "train_date":["2019-10-22","2019-10-23"],
                                #始发站2
                                "from_station":"杭州",
                                #到达站
                                "to_station":"北京",
                                #席别
                                "seats":["二等座",],
                                #出发时间段
                                "start_time_limit":[1,8],
                                #到达时间段
                                "arrive_time_limit":[18,22],
                            },

    }



    CHECKER.check_before_start(USER_DATA,QUERY_DATA)



