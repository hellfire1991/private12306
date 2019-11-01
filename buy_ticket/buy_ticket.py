from look_for_ticket.station import Station
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from verify.localVerifyCode import Verify

class BUY_TICKET(object):
    def __init__(self,user,query):
        self.user=user
        self.query=query
        #获取登陆完毕的浏览器
        self.driver=self.init_driver()
        self.prepare_to_buy()

    def init_driver(self):
        """
        初始化浏览器
        :return:
        """
        chrome_options = Options()
        #浏览器不加载图片
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def prepare_to_buy(self):
        """
        进入查询页面等待查询完毕
        :return:
        """
        self.driver.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc')
        time.sleep(3)
        # 填写出发站点,假点击，越过输入框无数据不能提交
        self.driver.find_element_by_css_selector("#fromStationText").click()
        self.driver.find_element_by_css_selector("#fromStationText").send_keys(self.query.get("from_station"))
        self.driver.find_element_by_css_selector("#citem_0").click()
        #为提交form 填写value,真数据
        from_station_key=Station.get_station_key_by_name(self.query.get("from_station"))
        javascript_message="var e=document.getElementById('fromStation').value="+"'"+from_station_key+"'"
        self.driver.execute_script(javascript_message)

        time.sleep(0.5)
        # 填写到达站点,假点击，越过输入框无数据不能提交
        self.driver.find_element_by_css_selector("#toStationText").click()
        self.driver.find_element_by_css_selector("#toStationText").send_keys(self.query.get("to_station"))
        self.driver.find_element_by_css_selector("#citem_0").click()

        # 为提交form 填写value,真数据
        to_station_key = Station.get_station_key_by_name(self.query.get("to_station"))
        javascript_message="var e=document.getElementById('toStation').value=" +"'"+ to_station_key+"'"
        self.driver.execute_script(javascript_message)

    def login(self):
        """
        登陆验证
        :return:
        """
        #选择使用账号密码登陆
        self.driver.find_element_by_css_selector(".login-hd-account").click()
        #等待验证码加载
        time.sleep(1)
        #验证登陆
        try:
            self.identify_image()
        except:
            pass
        finally:
            self.driver.find_element_by_css_selector("#J-userName").send_keys(self.user["user_name"], Keys.TAB, self.user["password"])
            self.driver.find_element_by_css_selector("#J-login").click()
        #等待页面跳转
        try:
            WebDriverWait(self.driver,4).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#submitOrder_id")))
        except:
            self.login()
        finally:
            #等待js数据加载
            time.sleep(0.5)
        #返回点击登陆后的url，如果登陆失败则无法进入正确的页面，检验登陆是否成功
        return True

    def identify_image(self):
        """
        识别验证码，并在浏览器上点击识别坐标
        :return:
        """
        image = self.driver.find_element_by_css_selector("#J-loginImg")
        src = image.get_attribute('src')
        img = src[22:]
        img_identify_result=Verify().verify(img)
        #判断是否识别并获取结果
        self.driver.maximize_window()
        if not img_identify_result:
            return None
        #根据验证码识别结果列表，分别在识别的点上打码（点击正确位置）
        while img_identify_result:
            local_x=img_identify_result[0]
            local_y=img_identify_result[1]
            #将打过的点在结果列表中去掉
            img_identify_result=img_identify_result[2:]
            #调用浏览器点击给定坐标的位置
            ActionChains(self.driver).move_to_element_with_offset(image, local_x, local_y).click().perform()
        return None

    def choose_seat(self):
        #提交订单前选座位
        self.driver.find_element_by_css_selector("#seatType_1").click()
        time.sleep(0.5)
        seat_type=self.mission[-1]
        seat_type_prepared=seat_type[0:2]
        seat_types=self.driver.find_elements_by_css_selector("#seatType_1 option")
        for seat_type in seat_types:
            seat_type_text=seat_type.text.lstrip()
            if seat_type_text[0:2]==seat_type_prepared:
                seat_type.click()
                break

    def choose_and_book(self):
        mission_date=self.mission[13]
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
        book_id = "#ticket_" + self.mission[2]
        selector_book = book_id + ">.no-br>.btn72"
        try:
            WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector_book)))
        finally:
            time.sleep(1)
            self.driver.find_element_by_css_selector(selector_book).click()
        try:
            WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR,".login-hd-account")))
        finally:
            time.sleep(1)
            return True

    def buy_ticket(self,mission):
        self.mission=mission
        #选择日期点击预定车票
        self.choose_and_book()
        #登陆验证
        self.login()
        # 选择乘车人
        self.driver.find_element_by_css_selector("#normal_passenger_id>li>input").click()
        time.sleep(0.5)
        #选择席别
        self.choose_seat()
        #提交订单
        self.driver.find_element_by_css_selector("#submitOrder_id").click()
        try:
            WebDriverWait(self.driver,4).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#confirmDiv")))
        finally:
            time.sleep(0.5)
            self.driver.find_element_by_css_selector("#confirmDiv .btn92s").click()
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".i-lock")))
        finally:
            return "succeeded"

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
