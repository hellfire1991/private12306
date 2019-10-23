from login.login import LOGIN_12306
from look_for_ticket.station import Station
import time

class BUY_TICKET(object):
    def __init__(self,user,query):
        self.user=user
        self.query=query
        #获取登陆完毕的浏览器
        self.driver=LOGIN_12306(self.user).__call__()
        #进入查询页面
        self.driver.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc')
        time.sleep(3)
        # 填写出发站点,假点击，越过输入框无数据不能提交
        self.driver.find_element_by_css_selector("#fromStationText").click()
        self.driver.find_element_by_css_selector("#fromStationText").send_keys(self.query.get("from_station"))
        self.driver.find_element_by_css_selector("#citem_0").click()
        #为提交form 填写value,真数据
        from_station_key=Station.get_station_key_by_name(self.query.get("from_station"))
        print(from_station_key)
        javascript_message="var e=document.getElementById('fromStation').value="+"'"+from_station_key+"'"
        self.driver.execute_script(javascript_message)

        time.sleep(0.5)
        # 填写到达站点,假点击，越过输入框无数据不能提交
        self.driver.find_element_by_css_selector("#toStationText").click()
        self.driver.find_element_by_css_selector("#toStationText").send_keys(self.query.get("to_station"))
        self.driver.find_element_by_css_selector("#citem_0").click()

        # 为提交form 填写value,真数据
        to_station_key = Station.get_station_key_by_name(self.query.get("to_station"))
        print(to_station_key)
        javascript_message="var e=document.getElementById('toStation').value=" +"'"+ to_station_key+"'"
        self.driver.execute_script(javascript_message)


    def re_init(self):
        self.driver=LOGIN_12306(self.user).__call__()
        self.driver.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc')
        time.sleep(3)
        # 填写出发站点
        self.driver.find_element_by_css_selector("#fromStationText").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("#fromStationText").send_keys(self.query.get("from_station"))
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("#citem_0").click()
        time.sleep(0.5)
        # 填写到达站点
        self.driver.find_element_by_css_selector("#toStationText").click()
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("#toStationText").send_keys(self.query.get("to_station"))
        time.sleep(0.5)
        self.driver.find_element_by_css_selector("#citem_0").click()
        print("买票模块准备完毕")

    def choose_seat(self,mission):
        #提交订单前选座位
        self.driver.find_element_by_css_selector("#ticketInfo_id").click()
        seat_type=mission[-1]
        seat_type_prepared=seat_type[0:1]
        seat_types=self.driver.find_elements_by_css_selector("#ticketInfo_id>option")
        for seat_type in seat_types:
            if seat_type.text[0:1]==seat_type_prepared:
                seat_type.click()
                break


    def buy_ticket(self,mission):
        self.mission=mission
        mission_date=mission[13]
        #生成网页车次日期选择器
        today_mday=time.localtime().tm_mday
        ticket_date_mday=int(mission_date[6:])
        selector_date="#date_range>ul li:nth-child"+"("+str(ticket_date_mday-today_mday+1)+")"
        #选择日趋
        self.driver.find_element_by_css_selector(selector_date).click()
        time.sleep(0.5)
        #车票预定选择器
        book_id="#ticket_"+self.mission[2]
        selector_book=book_id+">.no-br>.btn72"
        # 选择车票
        self.driver.find_element_by_css_selector(selector_book).click()
        time.sleep(2)
        # 选择乘车人
        self.driver.find_element_by_css_selector("#normal_passenger_id>li>input").click()
        time.sleep(0.5)
        self.choose_seat(mission)
        self.driver.find_element_by_css_selector("#submitOrder_id").click()
        time.sleep(2)
        # 确认订单
        # self.driver.find_element_by_css_selector("#confirmDiv .btn92s").click()

        return "succeeded"

    def __call__(self, *args, **kwargs):
        pass



if __name__=="__main__":
    buyer=BUY_TICKET()
    buyer.buy_ticket()
