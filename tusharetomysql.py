import tushare as ts
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
import pandas as pd

# 区间数据设定
e = pd.bdate_range('1/1/2020', '2/8/2021')
e.date #获取日期列表

pro = ts.pro_api('62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d')

for each in e.date:
    print(each.strftime("%Y%m%d"))
    df = pro.hk_hold(trade_date=each.strftime("%Y%m%d"), exchange='SH')
    engine = create_engine('mysql://root:admin123@127.0.0.1:3306/stock?charset=utf8')
    df.to_sql('hkholddata',engine,if_exists='append')
    df1 = pd.read_sql('hkholddata',engine)


