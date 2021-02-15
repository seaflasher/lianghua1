import tushare as ts
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
import pandas as pd

# 下载指定日期的港资持股比例
pro = ts.pro_api('62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d')
df = pro.hk_hold(trade_date='20210209', exchange='SZ')
engine = create_engine('mysql://root:admin123@127.0.0.1:3306/stock?charset=utf8')
df.to_sql('hkholddatamonth',engine,if_exists='append')
df1 = pd.read_sql('hkholddatamonth',engine)