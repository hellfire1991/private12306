from look_for_ticket.station import Station
from config import URL
from requests_html import  HTMLSession

class FIND_TICKET(object):
    """
    根据配置信息查询符合要求的票，并返回该票相应的数据
    """
    def __init__(self,query):
        #初始化长链接，并从配置中提取车次信息
        self.session=HTMLSession()
        self.prepare_session()
        self.train_date=query.get("train_date")
        self.from_station=query.get("from_station")
        self.to_station=query.get("to_station")
        self.seats=query.get("seats")
        self.start_time_limit=query.get("start_time_limit")
        self.arrive_time_limit=query.get("arrive_time_limit")
        self.query_url = self.prepare_query_url()
        self.query_time_out=10
        self.tickets_info=[]


    def query_by_date(self):
        #根据日期进行查询，返回原始数据
        res=[]
        for url in self.query_url:
            try:
                response=self.session.get(url)
            except:
                pass
            if response.status_code==200:
                r=response.json().get("data").get("result")
                res+=r
            elif response.status_code==302:
                #如果查询资源位置被修改，启用新的查询链接，特别注意：如果网站发生修改，出现了第三条尚未发现的查询链接，这里会进入死循环
                self.re_prepare_query_url()
                try:
                    res=self.query_by_date()
                except:
                    raise ("查询失败，12306查询链接可能已经失效，请联系作者")
                return res
        return res

    def get_tickets_info(self):
        #将查询到的票据原始数据处理成列表
        res=self.query_by_date()
        for res_item in res:
            ticket_info = res_item.split("|")
            self.tickets_info.append(ticket_info)
        return None


    def check_ticket_out(self):
        """对票据信息进行筛选，返回符合要求的票据信息
            单条车票信息列表中座席等级和列表下标的关系
            23——软卧
            25——特等座
            26——无座
            28——硬卧
            29——硬座
            30——二等座
            31——一等座
            32——商务座
        """
        mission_list=[]
        self.tickets_info_time_limited=[]
        for ticket_info in self.tickets_info:
            res=self.check_out_ticket_time_limited(ticket_info,self.start_time_limit,self.arrive_time_limit)
            if res:
                self.tickets_info_time_limited.append(ticket_info)
        if self.tickets_info_time_limited:
            pass
        else:
            raise ValueError("不存在车次符合您填写的发车/到达时间，请重新填写，或者查看12306官网后，选择合适的发车/到达时间")
        for ticket_info in self.tickets_info_time_limited:
            seats_needed = self.seats
            seats_index = self.get_seat_index(seats_needed)
            i=0
            for seat_index in seats_index:
                if ticket_info[seat_index]=="" or ticket_info[seat_index]=="无":
                    i+=1
                # elif ticket_info[seat_index]=="有":
                else:
                    mission=ticket_info
                    seat=self.get_seat_type(seat_index)
                    mission.append(seat)
                    # time_limit_check_result=self.check_out_ticket_time_limited(mission,self.start_time_limit,self.arrive_time_limit)
                    # if time_limit_check_result:
                    mission_list.append(mission)
            if mission_list:
                break

        return mission_list

    def prepare_session(self):
        #实例初始化时执行，为长连接获取查询前必须的cookies
        self.session.get(URL.get("API_PREPARE_QUERY_SESSION"))
        return None

    def prepare_query_url(self):
        #根据车次、站点、日期等信息创建查询链接
        base_query_url=URL.get("API_BASE_QUERY_URL_2")
        from_station_code=Station.get_station_key_by_name(self.from_station)
        to_station_code=Station.get_station_key_by_name(self.to_station)
        query_url=[]
        for date in self.train_date:
            url=base_query_url.format(train_date=date,from_staion_code=from_station_code,to_station_code=to_station_code)
            query_url.append(url)
        return query_url

    def re_prepare_query_url(self):
        #当车票信息资源位置被改变时，启用另外一个链接，针对查询 302 bug
        base_query_url = URL.get("API_BASE_QUERY_URL")
        from_station_code = Station.get_station_key_by_name(self.from_station)
        to_station_code = Station.get_station_key_by_name(self.to_station)
        query_url = []
        for date in self.train_date:
            url = base_query_url.format(train_date=date, from_staion_code=from_station_code,
                                        to_station_code=to_station_code)
            query_url.append(url)
        return query_url

    def check_out_ticket_time_limited(self,mission,start_time=None,arrive_time=None):
        s_time=start_time
        a_time=arrive_time
        mission_time_start=int(mission[8][0:2])
        mission_time_arrive=int(mission[9][0:2])

        start_time_checked_result=True
        arrive_time_checked_result=True
        check_result=True
        if s_time:
            if mission_time_start <= s_time[0] or mission_time_start >=s_time[1]:
                start_time_checked_result=False
        if a_time:
            if mission_time_arrive <= a_time[0] or mission_time_arrive >= a_time[1]:
                arrive_time_checked_result=False
        if start_time_checked_result and arrive_time_checked_result:
            return check_result



    def get_seat_index(self,seats):
        seats_name_index={"软卧":23,"特等座":25,"无座":26, "硬卧":28,"硬座":29,"二等座":30,"一等座":31,"商务座":32}
        seats_index=[]
        for seat in seats:
            seat_index=seats_name_index.get(seat)
            seats_index.append(seat_index)
        return seats_index

    def get_seat_type(self,index):
        seat_index_type={"23":"软卧","25":"特等座","26":"无座","28":"硬卧","29":"硬座","30":"二等座","31":"一等座","32":"商务座"}
        seat_type=seat_index_type.get(str(index))
        return seat_type

    def __call__(self, *args, **kwargs):
        #当有符合需求的票时，返回该条车票的数据
        self.get_tickets_info()
        return self.check_ticket_out()


if __name__=="__main__":
    pass
    # query={
    #                         #乘车日期
    #                         "train_date":["2019-10-25",],
    #                         #始发站2
    #                         "from_station":"杭州",
    #                         #到达站
    #                         "to_station":"北京",
    #                         #席别
    #                         "seats":["二等座",],
    #                         #出发时间段
    #                         "start_time_limit":[8,24],
    #                         #到达时间段
    #                         "arrive_time_limit":[18,22],
    #                     }
    # finder=FIND_TICKET(query)
    # res=finder()
    # for ticket in res:
    #     print(ticket)
    #
    #     print("出发时间：",ticket[8])
    #     print("到达时间：",ticket[9])


"""
座位和数据映射情况
23——软卧
25——特等座
26——无座
28——硬卧
29——硬座
30——二等座
31——一等座
32——商务座
"""

