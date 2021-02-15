import tushare as ts
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
import pandas as pd

# 区间数据设定
yearArray = [
    '2018',
    '2019',
    '2020',
    '2021',
]
monthArray = [
    '0101',
    '0115',
    '0201',
    '0215',
    '0301',
    '0315',
    '0401',
    '0415',
    '0501',
    '0515',
    '0601',
    '0615',
    '0701',
    '0715',
    '0801',
    '0815',
    '0901',
    '0915',
    '1001',
    '1015',
    '1101',
    '1115',
    '1201',
    '1215'
]


pro = ts.pro_api('62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d')

for year in yearArray:
    for month in monthArray:
        print(year+month)
        df = pro.hk_hold(trade_date=(year+month), exchange='SZ')
        engine = create_engine('mysql://root:admin123@127.0.0.1:3306/stock?charset=utf8')
        df.to_sql('hkholddatamonth',engine,if_exists='append')
        df1 = pd.read_sql('hkholddatamonth',engine)