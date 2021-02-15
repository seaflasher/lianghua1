import pandas as pd
e = pd.bdate_range('8/7/2019', '8/31/2019')
e.date #获取日期列表
for each in e.date:
    #print(type(each))
    print(each.strftime("%Y%m%d"))