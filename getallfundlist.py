import tushare as ts
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
import pandas as pd
import time

pro = ts.pro_api('62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d')
df = pro.fund_basic(market='E')
engine = create_engine('mysql://root:admin123@127.0.0.1:3306/stock?charset=utf8')

sleepCnt = 0

for index, row in df.iterrows():
    print(row['ts_code'])
    df1 = pro.fund_portfolio(ts_code=row['ts_code'])
    df1.to_sql('fundholddata',engine,if_exists='append')
    df1 = pd.read_sql('fundholddata',engine)
    sleepCnt = sleepCnt + 1
    if sleepCnt > 50:
        time.sleep(90)
        sleepCnt = 0