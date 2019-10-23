from app import APP


#用户账号密码（字典）
#多用户时，使用列表内嵌套用户信息字典表示
USER_DATA=[{"user_name":"hello","password":"xxxxxxxx"},]

#填写车票信息要注意严格按照模板填写，不然可能出现无法预测的bug
QUERY_DATA={"hello":{
                            #乘车日期(必填)
                            "train_date":["2019-10-23",],

                            #始发站2（必填）
                            "from_station":"杭州",

                            #到达站（必填）
                            "to_station":"北京",

                            #席别（土豪选填，不填就会有票就买，可能买到商务座，站票）
                            "seats":["二等座",],

                            #出发时间段（选填，可能半夜发车）
                            "start_time_limit":[6,8],

                            #到达时间段（选填）
                            # "arrive_time_limit":[18,22],
                        },

}

if __name__=="__main__":

    APP.start(USER_DATA,QUERY_DATA)