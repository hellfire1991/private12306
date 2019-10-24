from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from verify.localVerifyCode import Verify
class LOGIN_12306(object):

    def __init__(self,user):
        self.user_name=user.get("user_name")
        self.password=user.get("password")
        self.init_driver()

    def init_driver(self):
        #初始化浏览器，指向账号密码登陆页面

        chrome_options = Options()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        #浏览器进入首页，获取必要的cookies
        self.driver.get("https://www.12306.cn/index/index.html")
        time.sleep(8)
        login_entrence = self.driver.find_element_by_css_selector("#J-header-login>a")
        login_entrence.click()
        time.sleep(5)
        login_type = self.driver.find_element_by_css_selector(".login-hd-account>a")
        login_type.click()
        time.sleep(4)
        return None

    def login(self):
        #输入账号密码，验证完毕后点击登陆
        try:
            print("正在登陆")
            self.identify_image()
            time.sleep(3)
            self.driver.find_element_by_css_selector(".login-item>input").send_keys(self.user_name, Keys.TAB, self.password)
            login_buttun=self.driver.find_element_by_css_selector("#J-login")
            login_buttun.click()
            time.sleep(5)
        except:
            raise
        #返回点击登陆后的url，如果登陆失败则无法进入正确的页面，检验登陆是否成功
        return self.driver.current_url

    def relogin(self):
        try:
            print("正在登陆")
            self.identify_image()
            login_buttun=self.driver.find_element_by_css_selector("#J-login")
            login_buttun.click()
            time.sleep(5)
        except:
            raise
        #返回点击登陆后的url，如果登陆失败则无法进入正确的页面,用来检验登陆是否成功
        return self.driver.current_url



    def identify_image(self):
        #识别验证码，并在验证码正确位置点击
        image = self.driver.find_element_by_css_selector("#J-loginImg")
        src = image.get_attribute('src')
        img = src[22:]
        print(src)
        img_identify_result=Verify().verify(img)
        #判断是否识别并获取结果
        self.driver.maximize_window()
        if not img_identify_result:
            print('打码失败')
            return None
        #根据验证码识别结果列表，分别在识别的点上打码（点击正确位置）
        while img_identify_result:
            local_x=img_identify_result[0]
            local_y=img_identify_result[1]
            #将打过的点在结果列表中去掉
            img_identify_result=img_identify_result[2:]
            time.sleep(1)
            #调用浏览器点击给定坐标的位置
            ActionChains(self.driver).move_to_element_with_offset(image, local_x, local_y).click().perform()
        return None

    def __call__(self, *args, **kwargs):
        #返回登陆成功后的浏览器
        print("准备登陆")
        res=self.login()
        #判断登陆是否成功，失败则重新登陆
        while res != 'https://kyfw.12306.cn/otn/view/index.html':
            res=self.relogin()
            if res=='https://kyfw.12306.cn/otn/view/index.html':
                print("登陆成功")
            else:
                print("登陆失败，正在重新登陆")
        return self.driver

if __name__ =="__main__":
    pass
    # USER_DATA = [{"user_name": "hellfire1991", "password": "xxxxxxxx"},
    #              ]
    #
    # QUERY_DATA = {"hellfire1991": {
    #     "train_date": ["2019-10-10", ],
    #     "from_station": "杭州",
    #     "to_station": "昆明",
    #     "seats": ["二等座", ]
    # },
    # }
    #
    # user=USER_DATA[0]
    # login=LOGIN_12306(user)
    # login()
    #
