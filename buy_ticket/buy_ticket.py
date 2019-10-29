from login.login import LOGIN_12306
from look_for_ticket.station import Station
import time

class BUY_TICKET(object):
    def __init__(self,user,query):
        self.user=user
        self.query=query
        #获取登陆完毕的浏览器
        self.driver=LOGIN_12306(self.user).__call__()
        self.prepare_to_buy()

    def prepare_to_buy(self):
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

    def choose_seat(self,mission):
        #提交订单前选座位
        self.driver.find_element_by_css_selector("#seatType_1").click()
        time.sleep(3)
        seat_type=mission[-1]
        seat_type_prepared=seat_type[0:2]
        seat_types=self.driver.find_elements_by_css_selector("#seatType_1 option")
        for seat_type in seat_types:
            seat_type_text=seat_type.text.lstrip()
            if seat_type_text[0:2]==seat_type_prepared:
                seat_type.click()
                break


    def buy_ticket(self,mission):
        self.mission=mission
        mission_date=mission[13]
        #生成网页车次日期选择器
        # today_mday=time.localtime().tm_mday
        # ticket_date_mday=int(mission_date[6:])
        # selector_date="#date_range>ul li:nth-child"+"("+str(ticket_date_mday-today_mday+1)+")"
        # 选择日期
        # self.driver.find_element_by_css_selector(selector_date).click()
        #点击日历图标，弹出日期选择
        self.driver.find_element_by_css_selector("#date_icon_1").click()
        time.sleep(1)
        ticket_mon = mission_date[4:6]
        today_mon = str(time.localtime().tm_mon)
        ticket_date = mission_date[6:]
        #根据传入的任务日期查询当日车票信息
        if ticket_mon==today_mon:
            date_seclector = ".cal>.cal-cm div:nth-child(" + ticket_date + ")"
            date=self.driver.find_element_by_css_selector(date_seclector).click()
        else:

            date_seclector = ".cal-right>.cal-cm div:nth-child(" + ticket_date + ")"
            date=self.driver.find_element_by_css_selector(date_seclector).click()
        self.driver.find_element_by_css_selector("#query_ticket").click()
        time.sleep(1.5)
        #车票预定选择器
        book_id="#ticket_"+self.mission[2]
        selector_book=book_id+">.no-br>.btn72"
        # 选择车票
        self.driver.find_element_by_css_selector(selector_book).click()
        time.sleep(2)
        # 选择乘车人
        self.driver.find_element_by_css_selector("#normal_passenger_id>li>input").click()
        time.sleep(0.5)
        #选择席别
        self.choose_seat(self.mission)
        self.driver.find_element_by_css_selector("#submitOrder_id").click()
        time.sleep(2)
        # 确认订单
        self.driver.find_element_by_css_selector("#confirmDiv .btn92s").click()
        time.sleep(5)
        return "succeeded"

    def set_chrome_to_download_img(self):
        message='window.open("chrome://settings/content/images");'
        self.driver.execute_script(message)

    def __call__(self, *args, **kwargs):
        pass





if __name__=="__main__":
    user={"user_name":"hellfire1991","password":"xxxxxxxx"}
    query={
                            #乘车日期(必填)
                            "train_date":["2019-11-20",],

                            #始发站2（必填）
                            "from_station":"杭州",

                            #到达站（必填）
                            "to_station":"北京",

                            #席别（土豪选填，不填就会有票就买，可能买到商务座，站票）
                            "seats":["二等座",],

                            #出发时间段（选填，可能半夜发车）
                            "start_time_limit":[0,24],

                            #到达时间段（选填）
                            "arrive_time_limit":[0,24],
                        }
    buyer=BUY_TICKET(user,query)
