from app import APP


#用户账号密码（字典）
#多用户时，使用列表内嵌套用户信息字典表示
USER_DATA=[{"user_name":"hellfire1991","password":"XXXXXXXX"},]

#填写车票信息要注意严格按照模板填写，不然可能出现无法预测的bug
QUERY_DATA={"hellfire1991":{
                            #乘车日期(必填)
                            "train_date":["2019-11-25",],

                            #始发站2（必填）
                            "from_station":"杭州",

                            #到达站（必填）
                            "to_station":"北京",

                            #必填，可多选
                            "seats":["一等座",],

                            #乘客姓名(选填，不填默认买自己的票)，可以选择账号内的多个乘车人，不论单个还是多个，必须是列表
                            "passagers":["张三","李四"],

                            #出发时间段（选填，可能半夜发车）
                            "start_time_limit":[0,24],

                            #到达时间段（选填）
                            "arrive_time_limit":[0,24],
                        },

}

if __name__=="__main__":

    APP.start(USER_DATA,QUERY_DATA)