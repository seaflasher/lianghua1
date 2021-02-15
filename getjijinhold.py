import os
import pandas as pd
import tushare as ts
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib as mpl
from cycler import cycler# 用于定制线条颜色
import time

def get_jijin_csv():
    pro = ts.pro_api('62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d')
    jiJinFile = 'jiJin.csv'
    if not os.path.exists(jiJinFile):
        df = pro.fund_basic(market='E')
        df.to_csv(jiJinFile, encoding='utf_8_sig')
    df = pd.read_csv(jiJinFile)
    path = 'd:/stockdata/jijin/'
    dir = Path(path)
    if not os.path.exists(dir):
        os.mkdir(dir)
    codes = df['ts_code'].values
    names = df['name'].values
    fund_types = df['fund_type'].values
    for code, name, fund_type in zip(codes, names, fund_types):
        if fund_type == '商品型' or fund_type == '债券型' or '货币市场型' == fund_type:
            continue
        jijin_chicang_file = path + code +'_'+ name + '.csv'
        if not os.path.exists(jijin_chicang_file):
            df = pro.fund_portfolio(ts_code=code)
            df.to_csv(jijin_chicang_file, encoding='utf_8_sig')
            time.sleep(1)


# 加载股票列表
def load_code_list(market='SZSE', sel=False):    #交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
    path = './data/'
    faceDir = Path(path)
    if faceDir.exists():
        file_dir = path + 'code_list_' + market + '.csv'
    else:
        os.mkdir(faceDir)
        file_dir = path + 'code_list_' + market + '.csv'
    # 判断文件是否存在,不存在则通过网络接口获得
    if os.path.exists(file_dir):
        code_list = pd.read_csv(file_dir)
    else:
        # 初始化pro接口
        pro = ts.pro_api('ee5c0e991e17949cdafbcf8ec42321ef4bac94e9ca3474e4d62313a3')
        # 查询某交易所所有上市公司
        #code_list = pro.stock_basic(exchange=market, list_status='L', fields='ts_code')  # ,symbol,name,market,list_date
        #code_list = pro.stock_basic(exchange=market, list_status='L')  # ,symbol,name,market,list_date
        code_list = pro.stock_basic(exchange=market, list_status='L')  # ,symbol,name,market,list_date

        # 保存数据到文件
        code_list.to_csv(file_dir, index=False, encoding="utf_8_sig")

    #code_list = code_list[['ts_code']].values.flatten()
    return code_list


#获取代码对应的名字
def get_code_name(ts_code):

    code_list = pd.read_csv('all_codes.csv')
    codes = code_list['ts_code'].values
    names = code_list['name'].values
    i = 0
    for code in codes:
        if code == ts_code:
            return names[i]
        else:
            i = i+1
    print('NOName ************************** NoName')
    return 'noName'

#获取名字对应代码
def get_name_code(name):


    code_list = pd.read_csv('all_codes.csv')
    codes = code_list['ts_code'].values
    names = code_list['name'].values
    i = 0
    for find in names:
        if name == find:
            return codes[i]
        else:
            i = i+1

    print('NOCode ************************** NOCode')
    return 'NoCode'



# 获取单个代码的总值##############################################################
def get_code_in_jijin_perValue(ts_code, is_debug = False):
    pro = ts.pro_api('ee5c0e991e17949cdafbcf8ec42321ef4bac94e9ca3474e4d62313a3')
    jiJinFile = 'jiJin.csv'
    if not os.path.exists(jiJinFile):
        df = pro.fund_basic(market='E')
        df.to_csv(jiJinFile, encoding='utf_8_sig')
    df = pd.read_csv(jiJinFile)
    path = './基金/'
    dir = Path(path)
    if not os.path.exists(dir):
        os.mkdir(dir)
    jijin_codes = df['ts_code'].values
    jijin_names = df['name'].values
    fund_types = df['fund_type'].values

    ts_name = get_code_name(ts_code)
    per_value = 0
    mkv_value = 0
    count = 0
    for jijin_code, jiJin_name, fund_type in zip(jijin_codes, jijin_names, fund_types):
        if fund_type == '商品型' or fund_type == '债券型' or '货币市场型' == fund_type:
            continue
        jijin_chicang_file = path + jijin_code + '_' + jiJin_name + '.csv'
        if not os.path.exists(jijin_chicang_file):
            df = pro.fund_portfolio(ts_code=ts_code)
            df.to_csv(jijin_chicang_file, encoding='utf_8_sig')
            #time.sleep(1)
        jijin_df = pd.read_csv(jijin_chicang_file)
        gupiao_codes = jijin_df['symbol'].values  #代码
        stk_float_ratios = jijin_df['stk_float_ratio'].values   #占流通市值比例
        ann_dates = jijin_df['ann_date'].values  # 公告日
        stk_mkv_ratios = jijin_df['stk_mkv_ratio'].values  #占股票市值比

        isFind = False
        for i in range(len(gupiao_codes)):
            if ann_dates[i] != ann_dates[0]:
                break
            if ts_code == gupiao_codes[i]:
                per_value = per_value + stk_float_ratios[i]
                mkv_value = mkv_value + stk_mkv_ratios[i]
                count = count +1
                isFind = True

        if is_debug and isFind:
            print('jiJin', jijin_code, jiJin_name, ts_code, ts_name, '%.2f'% per_value)
    print("Count",count, ts_code, ts_name,  '%.2f'% per_value)
    return per_value, count, mkv_value



def get_allcode_per_value():

    code_list = pd.read_csv('all_codes.csv')
    codes = code_list['ts_code'].values
    names = code_list['name'].values
    markets = code_list['market'].values

    code_array = np.array([])
    name_array = np.array([])
    per_array = np.array([])
    count_array = np.array([])
    mkv_array = np.array([])

    writefile = 'all_code_fund_value.csv'

    for code, market, name in zip(codes, markets, names):

        if market == '科创板':
            print(market, code, name)
            continue


        # 获取单个代码的总值##############################################################
        per_value, count, mkv_value = get_code_in_jijin_perValue(code)
        code_array = np.append(code_array, code)
        name_array = np.append(name_array, name)
        per_array = np.append(per_array, per_value)
        count_array = np.append(count_array, count)
        mkv_array = np.append(mkv_array, mkv_value)

        data = [code_array, name_array, count_array, per_array]
        data = np.transpose(data)
        ser2 = pd.DataFrame(data, columns=['ts_code', 'name', 'count', 'per_value'])


        ser2.to_csv(writefile, encoding="utf_8_sig")
    print("EEEEEEEEE")

#get_code_in_jijin_perValue('600837.SH', is_debug = True)
get_allcode_per_value()