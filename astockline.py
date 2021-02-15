import tushare as ts
import pandas as pd

pro = ts.pro_api('62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d')

#上证涨幅资金
#df = pro.index_basic(ts_code='000001.SZ', start_date='20100201', end_date='20210128')
#df.to_excel('test0.xlsx')

#沪港通等资金流向
#df = pro.moneyflow_hsgt(start_date='20180125', end_date='20210208')
#df.to_excel('test1.xlsx')

#获取单日全部持股
#df = pro.hk_hold(trade_date='20210208')
df = pro.hk_hold(trade_date='20180208', exchange='SH')
df.to_excel('test3.xlsx')

#获取单日交易所所有持股
#df = pro.hk_hold(trade_date='20190625', exchange='SH')
#df.to_excel('test3.xlsx')

#df = pro.query('top_inst', trade_date='20210208', ts_code='000858.SZ')
#df.to_excel('test2.xlsx')