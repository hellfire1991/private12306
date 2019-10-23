from os import path
import random
#车票信息


#设置静态文件路径
BASE_PATH=path.dirname(path.dirname(path.abspath(__file__))) + '/my12306/'
PATH={
    "stations_path":BASE_PATH+"necessary_data/station.txt",
    "log_path":BASE_PATH+"log/",

}

#设置URL_API
HOST_URL_OF_12306 = 'kyfw.12306.cn'
BASE_URL_OF_12306 = 'https://' + HOST_URL_OF_12306
URL = {

    "API_FREE_CODE_QCR_API": 'https://12306-ocr.pjialin.com/check/',

    "API_NOTIFICATION_BY_VOICE_CODE": 'http://ali-voice.showapi.com/sendVoice?',

    "API_NOTIFICATION_BY_VOICE_CODE_DINGXIN": 'http://yuyin2.market.alicloudapi.com/dx/voice_notice',

    "API_CHECK_CDN_AVAILABLE": 'https://{}/otn/dynamicJs/omseuuq',
#我自己加的
    "API_PREPARE_QUERY_SESSION":"https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc",
    "API_BASE_QUERY_URL":"https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_staion_code}&leftTicketDTO.to_station={to_station_code}&purpose_codes=ADULT",
    "API_BASE_QUERY_URL_2": "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_staion_code}&leftTicketDTO.to_station={to_station_code}&purpose_codes=ADULT",

}