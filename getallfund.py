import tushare as ts

pro = ts.pro_api('62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d')
df = pro.fund_basic()
df.to_excel('d:/stockdata/fundlist.xlsx')