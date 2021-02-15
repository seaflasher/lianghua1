import tushare as ts

pro = ts.pro_api('62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d')
df = pro.index_daily(ts_code='000001.sh', start_date='20100201', end_date='20210201')
df.to_excel('d:/stockdata/test0.xlsx')