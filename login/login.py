import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from verify.localVerifyCode import Verify
class LOGIN_12306(object):

    def __init__(self,user):
        self.user_name=user.get("user_name")
        self.password=user.get("password")
        self.init_driver()

    def init_driver(self):
        #初始化浏览器，指向账号密码登陆页面

        chrome_options = Options()
        #浏览器不加载图片
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)
        #浏览器进入首页，获取必要的cookies
        self.driver.get("https://www.12306.cn")
        #等待必要数据加载完毕，登陆标签出现
        try:
            WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#J-header-login>a")))
        finally:
            #等待加载js数据
            time.sleep(3)
            self.driver.find_element_by_css_selector("#J-header-login>a").click()
        #等待选择登陆方式标签出现
        try:
            WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".login-hd-account>a")))
        finally:
            #等待加载js数据
            time.sleep(1)
            self.driver.find_element_by_css_selector(".login-hd-account>a").click()
            #等待加载验证码
            time.sleep(1)
        return None

    def login(self):
        #输入账号密码，验证完毕后点击登陆
        try:
            print("正在登陆")
            self.identify_image()
        except:
            raise Exception("登陆失败")
        finally:
            self.driver.find_element_by_css_selector(".login-item>input").send_keys(self.user_name, Keys.TAB, self.password)
            login_buttun=self.driver.find_element_by_css_selector("#J-login")
            login_buttun.click()
        #等待欢迎页面加载成功
        try:
            WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".welcome-tit")))
        except:
            return False
        finally:
            #等待js数据加载
            time.sleep(1)
        #返回点击登陆后的url，如果登陆失败则无法进入正确的页面，检验登陆是否成功
        return True

    def relogin(self):
        self.driver.find_element_by_css_selector(".lgcode-refresh").click()
        time.sleep(1)
        try:
            print("正在登陆")
            self.identify_image()
        except:
            raise Exception("登陆失败")
        finally:
            self.driver.find_element_by_css_selector(".login-item>input").send_keys(self.user_name, Keys.TAB, self.password)
            login_buttun=self.driver.find_element_by_css_selector("#J-login")
            login_buttun.click()
        #等待欢迎页面加载成功
        try:
            WebDriverWait(self.driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".welcome-tit")))
        except:
            return False
        finally:
            #等待js数据加载
            time.sleep(1)
        #返回点击登陆后的url，如果登陆失败则无法进入正确的页面，检验登陆是否成功
        return True
    def identify_image(self):
        #识别验证码，并在验证码正确位置点击
        image = self.driver.find_element_by_css_selector("#J-loginImg")
        src = image.get_attribute('src')
        img = src[22:]
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
            #调用浏览器点击给定坐标的位置
            ActionChains(self.driver).move_to_element_with_offset(image, local_x, local_y).click().perform()
        return None

    def __call__(self, *args, **kwargs):
        #返回登陆成功后的浏览器
        print("准备登陆")
        res=self.login()
        #判断登陆是否成功，失败则重新登陆
        while not res:
            res=self.relogin()
            if res:
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
