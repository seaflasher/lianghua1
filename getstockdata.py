import os
import pandas as pd
import tushare as ts
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib as mpl
from cycler import cycler  # 用于定制线条颜色
import time


# 获取一支股票的历史数据
def load_data(ts_code, start_date='20160101', end_date=''):
    # 判断文件是否存在,不存在则通过网络接口获得
    data_dir = 'd:/stockdata/'
    if not os.path.exists(data_dir + ts_code + '.csv'):

        # 初始化pro接口
        pro = ts.pro_api('62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d')
        # 获取前复权数据
        df = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, ma=[5, 10, 20, 30, 50, 120, 200])

        # 保存数据到文件
        if df is None:
            print('can not get data')
            return
        df.to_csv(data_dir + ts_code + '.csv', index=False, encoding="utf_8_sig")
        print('new file', ts_code)
    df = pd.read_csv(data_dir + ts_code + '.csv')
    # ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount, adj_factor
    # 股票代码, 交易日期, 开盘价, 最高价, 最低价, 收盘价, 昨收价, 涨跌额, 涨跌幅, 成交量, 成交额(千元)
    # 去空
    df.dropna(inplace=True)
    # 正序
    df = df.sort_index(ascending=False)
    # 索引重排序
    df.reset_index(drop=True, inplace=True)
    return df


# 加载股票列表
def load_code_list(market='SZSE', sel=False):  # 交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
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
        # code_list = pro.stock_basic(exchange=market, list_status='L', fields='ts_code')  # ,symbol,name,market,list_date
        # code_list = pro.stock_basic(exchange=market, list_status='L')  # ,symbol,name,market,list_date
        code_list = pro.stock_basic(exchange=market, list_status='L')  # ,symbol,name,market,list_date

        # 保存数据到文件
        code_list.to_csv(file_dir, index=False, encoding="utf_8_sig")

    # code_list = code_list[['ts_code']].values.flatten()
    return code_list


def all_test(codes, names, days, begin_count, end_count, earnings_count=30, writefile='codes.csv'):
    count_earnings = 0
    count_suc = 0
    count_fail = 0

    earnings_count = (end_count - begin_count) * 0.1

    name_array = np.array([])
    code_array = np.array([])
    suc_array = np.array([])
    fail_array = np.array([])
    earnings_array = np.array([])

    # for code in codes:
    for i in range(len(codes)):
        earnings, suc, fail, index_array, pct_array = test(codes[i], days=days, begin_count=begin_count,
                                                           end_count=end_count, name=names[i])
        if suc == -1:
            continue
        count_earnings = count_earnings + earnings
        count_suc = count_suc + suc
        count_fail = count_fail + fail

        if earnings > earnings_count:
            # print('test == ', code, suc, fail, price)
            name_array = np.append(name_array, names[i])
            code_array = np.append(code_array, codes[i])
            suc_array = np.append(suc_array, suc)
            fail_array = np.append(fail_array, fail)
            earnings_array = np.append(earnings_array, earnings)

        print('count_suc', count_suc)
        print('count_fail', count_fail)
        print('count_earnings', count_earnings)
        print("suc ", count_suc / (count_suc + count_fail + 1) * 100)

        print("earnings pre ", i, count_earnings / (count_suc + count_fail + 1))

    data = [code_array, name_array, suc_array, fail_array, earnings_array]
    data = np.transpose(data)
    ser2 = pd.DataFrame(data, columns=['ts_code', 'name', 'suc', 'fail', 'earnings'])
    # ser2 = pd.Series(suc_array)
    # ser2 = pd.Series(fail_array)
    # ser2 = pd.Series(price_array)
    ser2.to_csv(writefile, encoding="utf_8_sig")


def test_sel_codes(days, begin_count, end_count, names, file='codes.csv'):
    df = pd.read_csv(file)
    codes = df['ts_code'].values
    names = df['name'].values

    print(codes)
    all_test(codes, names=names, days=days, begin_count=begin_count, end_count=end_count)


def sel_current_code(ts_codes, name='no_name'):
    df = load_data(ts_codes)

    i = -1
    begin_count = -3
    end_count = -1

    date = df['trade_date'].values[begin_count:]
    close = df['close'].values[begin_count:]

    price = 25
    if close.mean() < price:
        return False, '1999'

    change = df['change'].values[begin_count:]
    pct_change = df['pct_chg'].values[begin_count:]
    vol = df['vol'].values[begin_count:]
    ma5 = df['ma5'].values[begin_count:]
    ma10 = df['ma10'].values[begin_count:]
    ma20 = df['ma20'].values[begin_count:]
    ma30 = df['ma30'].values[begin_count:]
    ma50 = df['ma50'].values[begin_count:]
    ma120 = df['ma120'].values[begin_count:]
    ma200 = df['ma200'].values[begin_count:]

    ma_v_5 = df['ma_v_5'].values[begin_count:]
    ma_v_10 = df['ma_v_10'].values[begin_count:]
    ma_v_20 = df['ma_v_20'].values[begin_count:]
    ma_v_30 = df['ma_v_30'].values[begin_count:]
    ma_v_50 = df['ma_v_50'].values[begin_count:]
    ma_v_120 = df['ma_v_120'].values[begin_count:]

    if len(close) < 2:
        return False, '1999'

    condition0 = close[i] > ma5[i]

    condition1 = ma5[i] < ma10[i]
    condition2 = ma10[i] < ma20[i]

    condition_0 = ma5[i] > ma5[i - 1]
    condition_1 = ma10[i] > ma10[i - 1]
    condition3 = ma20[i] > ma30[i]
    condition_2 = ma20[i] > ma20[i - 1]

    condition4 = ma30[i] > ma50[i]
    condition5 = ma50[i] > ma120[i]
    condition6 = ma120[i] > ma200[i]

    condition11 = ma_v_5[i] > ma_v_5[i - 1]
    condition12 = ma_v_5[i] > ma_v_10[i]
    condition13 = ma_v_5[i] > ma_v_20[i]
    condition14 = ma_v_10[i] > ma_v_30[i]
    condition15 = ma_v_20[i] > ma_v_50[i]
    condition16 = ma_v_50[i] > ma_v_120[i]

    conditionOne = pct_change[i] < 9.5
    conditionTwo = pct_change[i + 1] < 9.5

    if conditionOne and conditionTwo:  # pct_change[i+1] < 9.5  表示下一个交易日 涨停
        power = 1.2
        buys, sells = check_days_money(ts_codes, name, date[i], days=5)

        if buys / (sells + 1) > power:
            print(ts_codes, name, buys, sells, '%.1f' % (buys / sells * 100))
            return True, date[i]

    # if close[i] > ma5[i] and close[i - 1] < ma5[i - 1] and pct_change[i] < 9.5:  # pct_change[i] < 9.5 当日交易 涨停

    return False, date[i]


def all_sel_current_code(codes, names, writefileName='sel_codes.csv', writefile=True):
    path = './选择/'
    dir = Path(path)
    if not dir.exists():
        os.mkdir(dir)

    begin_count = -100
    end_count = -1
    days = 20

    name_array = np.array([])
    code_array = np.array([])
    date_array = np.array([])

    for i in range(len(codes)):
        code = codes[i]
        name = names[i]
        # 判断条件选择
        ret, date = sel_current_code(code, name)
        if ret:
            name_array = np.append(name_array, name)
            code_array = np.append(code_array, code)
            date_array = np.append(date_array, date)

            # for code, name in zip(codes, names):

            earnings, suc, fail, index_array, pct_array = test(code, name=name, days=days, begin_count=begin_count,
                                                               end_count=end_count)
            if suc == -1:
                continue
            name = str.replace(name, '*', ' ')
            if earnings > 0:
                file_dir = path + 'Curent_AAA_%s_%s %d %d++%.1f++%.1f.png' % (
                code, name, suc, fail, suc * 100 / (fail + suc + 1), earnings)
            else:
                file_dir = path + 'Curent_BBB_%s_%s %d %d——%.1f——%.1f.png' % (
                code, name, suc, fail, suc * 100 / (fail + suc + 1), earnings)
            plot_pct(code, index_array, pct_array, begin_count=begin_count, end_count=end_count, writefilename=file_dir)
            print("codes %s %s earnings %.2f" % (code, name, earnings))

    data = [code_array, name_array, date_array]
    data = np.transpose(data)  # 矩阵转置
    ser2 = pd.DataFrame(data, columns=['ts_code', 'name', 'date'])
    # ser2 = pd.Series(suc_array)
    # ser2 = pd.Series(fail_array)
    # ser2 = pd.Series(price_array)
    if writefile:
        ser2.to_csv(writefileName, encoding="utf_8_sig")


def draw_finance(ts_codes, begin_count, end_count=-1):
    df = load_data(ts_codes)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    opens = df['open'].values[begin_count:end_count]
    closes = df['close'].values[begin_count:end_count]
    highs = df['high'].values[begin_count:end_count]
    lows = df['low'].values[begin_count:end_count]
    dates = df['trade_date'].values[begin_count:end_count]
    vols = df['vol'].values[begin_count:end_count]

    data = [dates, opens, closes, highs, lows, vols]
    data = np.transpose(data)  # 矩阵转置

    df = pd.DataFrame(data, columns=['Date', 'Open', 'Close', 'High', 'Low', 'Volume'])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index(['Date'], inplace=True)
    # df.index.name = 'Date'

    # 设置基本参数
    # type:绘制图形的类型, 有candle, renko, ohlc, line等
    # 此处选择candle,即K线图
    # mav(moving average):均线类型,此处设置7,30,60日线
    # volume:布尔类型，设置是否显示成交量，默认False
    # title:设置标题
    # y_label:设置纵轴主标题
    # y_label_lower:设置成交量图一栏的标题
    # figratio:设置图形纵横比
    # figscale:设置图形尺寸(数值越大图像质量越高)
    kwargs = dict(
        type='candle',
        mav=(5, 10, 20),
        volume=True,
        title='\nA_stock %s candle_line' % (ts_codes),
        ylabel='OHLC Candles',
        ylabel_lower='Shares\nTraded Volume',
        figratio=(50, 30),
        figscale=15)

    # 设置marketcolors
    # up:设置K线线柱颜色，up意为收盘价大于等于开盘价
    # down:与up相反，这样设置与国内K线颜色标准相符
    # edge:K线线柱边缘颜色(i代表继承自up和down的颜色)，下同。详见官方文档)
    # wick:灯芯(上下影线)颜色
    # volume:成交量直方图的颜色
    # inherit:是否继承，选填
    mc = mpf.make_marketcolors(
        up='red',
        down='green',
        edge='i',
        wick='i',
        volume='in',
        inherit=True)

    # 设置图形风格
    # gridaxis:设置网格线位置
    # gridstyle:设置网格线线型
    # y_on_right:设置y轴位置是否在右
    s = mpf.make_mpf_style(
        gridaxis='both',
        gridstyle='-.',
        y_on_right=False,
        marketcolors=mc)
    # 设置均线颜色，配色表可见下图
    # 建议设置较深的颜色且与红色、绿色形成对比
    # 此处设置七条均线的颜色，也可应用默认设置
    mpl.rcParams['axes.prop_cycle'] = cycler(
        color=['dodgerblue', 'deeppink',
               'navy', 'teal', 'maroon', 'darkorange',
               'indigo'])

    # 设置线宽
    mpl.rcParams['lines.linewidth'] = .5

    # 图形绘制
    # show_nontrading:是否显示非交易日，默认False
    # savefig:导出图片，填写文件名及后缀
    mpf.plot(df,
             **kwargs,
             style=s,
             show_nontrading=False,
             savefig='%s_begin%d_end%d'
                     % (ts_codes, begin_count, end_count) + '.png')

    # candlestick2_ochl(ax, opens=opens, closes=closes, highs=highs, lows=lows, width=0.75, colorup='red', colordown='green')
    # plt.legend(loc= 'best')
    # plt.xticks(range(len(date)), date, rotation=30)
    # plt.grid(True)
    # plt.title(ts_codes)

    # plt.show


def plot_pct(ts_code, index_array, pct_array, begin_count, end_count=-1, writefilename='temp.png'):
    df = load_data(ts_code)

    closes = df['close'].values

    ma5 = df['ma5'].values
    ma10 = df['ma10'].values
    ma20 = df['ma20'].values

    if len(closes) + 1 < abs(begin_count):
        print("TTTTTTT", len(closes), begin_count, ts_code)
        begin_count = int(len(closes) * -1)
    if len(closes) < end_count * -1:
        end_count = -1

    if begin_count + 30 > end_count:
        return

    x_array = np.linspace(begin_count, end_count, end_count - begin_count, dtype=np.int)
    l = len(ma5)
    x = len(x_array)
    print('len', l, x)

    ma5Mean_array = np.linspace(ma5.mean(), ma5.mean(), end_count - begin_count)
    # plt.plot(x_array, closes, c='black')

    start_date = df['trade_date'].values[begin_count]
    end_date = df['trade_date'].values[end_count]

    print(start_date, end_date)

    name = get_code_name(ts_code)
    money_df = get_dates_money(code=ts_code, name=name)
    # print(money_df)
    name = name.replace('*', " ")
    # money_df.to_csv(ts_code+ name+ "moneydf.csv", encoding='utf_8_sig')

    money_dates = money_df['trade_date'].values

    # 日期对齐
    bi = 0
    for date in money_dates:
        if date == start_date:
            break
        else:
            bi = bi + 1

    if bi < -1 * len(money_dates):
        print("BB日期对齐出错")
        return 0, 0

    ei = 0
    for date in money_dates:
        if date == end_date:
            break
        else:
            ei = ei + 1

    if ei < -1 * len(money_dates):
        print("EE日期对齐出错")
        return 0, 0
    # 日期对齐
    bi = bi
    ei = ei
    # print(bi, ei, start_date, end_date)

    # buys, sells = check_days_money(ts_code, name, date[i], days=5)

    plt.figure(figsize=(30, 18))
    plt.grid()

    if money_df is not None:
        buy_lg_vol = money_df['buy_lg_vol'].values[bi:ei]
        sell_lg_vol = money_df['sell_lg_vol'].values[bi:ei]
        buy_elg_vol = money_df['buy_elg_vol'].values[bi:ei]
        sell_elg_vol = money_df['sell_elg_vol'].values[bi:ei]

        buys = buy_lg_vol + buy_elg_vol
        sells = sell_lg_vol + sell_elg_vol

        changeBuys = buys * 5
        days = 5
        for k in range(days - 1, len(buys)):
            temp = 0
            for i in range(days):
                temp = temp + buys[k - i]
            changeBuys[k] = temp

            # print('buys', k, changeBuys[k], dates[k])
            # tempBuy = 0

        changeSells = buys * 5

        for k in range(days - 1, len(sells)):
            temp = 0
            for i in range(days):
                temp = temp + sells[k - i]
            changeSells[k] = temp

            # print('sell', k, changeSells[k], dates[k])

        pers = (changeBuys) / (changeSells + 1)

        percount = pers * ma5.mean()

        if len(pers) <= 10:
            return

        days = 5
        # for d in range(days):
        #    percount[d] = percount[d] * days
        # for d in range(0, len(pers)):
        #    for b in range(1, days):
        #       percount[d] = percount[d] + pers[d-b]
        #
        # print(pers)
        # print(pers)

        # percount = percount / days

        # print(closes)
        # print(pers)

        plt.plot(x_array, ma5Mean_array, c='yellow')
        if len(x_array) == len(percount):
            plt.plot(x_array, percount, c='black')

    plt.plot(x_array, closes[begin_count:end_count], c='r')
    plt.plot(x_array, ma5[begin_count:end_count], c='g')
    plt.plot(x_array, ma10[begin_count:end_count], c='b')
    plt.plot(x_array, ma20[begin_count:end_count], c='y')

    xtick = np.arange(begin_count, end_count + 1, 20, dtype=np.int)

    plt.xticks(xtick)

    for index, pct in zip(index_array, pct_array):

        c = closes[int(index)]
        if pct < 0:
            # plt.quiver(index, c, 0, 1, color='g', )
            plt.text(index, c, s='%.1f' % pct, alpha=0.5, backgroundcolor='g')
        else:
            # plt.quiver(index, c, 0, 1, color='r', )
            plt.text(index, c, s='%.1f' % pct, alpha=0.5, backgroundcolor='r')
    # plt.title('%s suc %d fail %d %.1f' % (ts_codes, suc, fail, earnings))
    # plt.plot(index_array, pct_array, 'om')
    plt.savefig(writefilename, format='png')
    # plt.show()
    plt.close()


def all_plot_pct(codes, names, days, begin_count, end_count=-1):
    path = './image/'
    Dir = Path(path)
    if not Dir.exists():
        os.mkdir(Dir)
    # file = path + code
    # df = pd.read_csv(file)
    # codes = df['ts_code'].values[begin_count:end_count]
    i = 0

    count_earnings = 0
    count_suc = 0
    count_fail = 0
    for code, name in zip(codes, names):
        i = i + 1
        earnings, suc, fail, index_array, pct_array = test(code, name=name, days=days, begin_count=begin_count,
                                                           end_count=end_count)
        if suc == -1:
            continue
        name = str.replace(name, '*', ' ')
        if earnings > 0:
            file_dir = path + 'AAA_%s_%s %d %d++%.1f++%.1f.png' % (
            code, name, suc, fail, suc * 100 / (fail + suc + 1), earnings)
        elif earnings < -0.01:
            file_dir = path + 'BBB_%s_%s %d %d——%.1f——%.1f.png' % (
            code, name, suc, fail, suc * 100 / (fail + suc + 1), earnings)
        else:
            file_dir = path + 'OOO_%s_%s %d %d——%.1f——%.1f.png' % (
            code, name, suc, fail, suc * 100 / (fail + suc + 1), earnings)
        plot_pct(code, index_array, pct_array, begin_count=begin_count, end_count=end_count, writefilename=file_dir)
        print("codes %s %s earnings %.2f" % (code, name, earnings))

        count_earnings = count_earnings + earnings
        count_suc = count_suc + suc
        count_fail = count_fail + fail

        print('count_suc', count_suc)
        print('count_fail', count_fail)
        print('count_earnings', count_earnings)
        print("suc ", count_suc / (count_suc + count_fail + 1) * 100)
        print("earnings pre ", i, count_earnings / (count_suc + count_fail + 1))


def test_plot():
    # 绘制曲线
    x = np.linspace(2, 21, 20)  # 取闭区间[2, 21]之间的等差数列，列表长度20
    y = np.log10(x) + 0.5
    plt.figure()  # 添加一个窗口。如果只显示一个窗口，可以省略该句。
    plt.plot(x, y)  # plot在一个figure窗口中添加一个图，绘制曲线，默认颜色

    # 绘制离散点
    plt.plot(x, y, '.y')  # 绘制黄色的点，为了和曲线颜色不一样
    x0, y0 = 15, np.log10(15) + 0.5
    plt.annotate('Interpolation point', xy=(x0, y0), xytext=(x0, y0 - 1), arrowprops=dict(arrowstyle='->'))  # 添加注释
    for x0, y0 in zip(x, y):
        plt.quiver(x0, y0 - 0.3, 0, 1, color='g', width=0.005)  # 绘制箭头

    x = range(2, 21, 5)
    y = np.log10(x) + 0.5
    plt.plot(x, y, 'om')  # 绘制紫红色的圆形的点
    x0, y0 = 7, np.log10(7) + 0.5
    plt.annotate('Original point', xy=(x0, y0), xytext=(x0, y0 - 1), arrowprops=dict(arrowstyle='->'))
    for x0, y0 in zip(x, y):
        plt.quiver(x0, y0 + 0.3, 0, -1, color='g', width=0.005)  # 绘制箭头

    # 设置坐标范围
    plt.xlim(2, 21)  # 设置x轴范围
    plt.xticks(range(0, 23, 2))  # 设置X轴坐标点的值，为[0， 22]之间的以2为差值的等差数组
    plt.ylim(0, 3)  # 设置y轴范围

    # 显示图形
    plt.show()  # 显示绘制出的图


# test_plot()
def in_longhu(ts_code, date):
    date = str(date)
    y = date[0:4]
    m = date[4:6]
    d = date[6:8]

    global market

    # date = y + '-' + m + '-' + d

    path = './longhudata/'
    faceDir = Path(path)
    if faceDir.exists():
        file_dir = path + market + date + '.csv'
    else:
        os.mkdir(faceDir)
        file_dir = path + market + date + '.csv'
    # 判断文件是否存在,不存在则通过网络接口获得
    if os.path.exists(file_dir):
        df = pd.read_csv(file_dir)
        codes = df['ts_code'].values
    else:
        # 初始化pro接口
        pro = ts.pro_api('ee5c0e991e17949cdafbcf8ec42321ef4bac94e9ca3474e4d62313a3')
        df = pro.top_list(trade_date=date)
        df.to_csv(file_dir, index=False, encoding="utf_8_sig")
        codes = df['ts_code'].values
        # print(codes)

    for c in codes:
        if c == ts_code:
            print(c, ts_code, date, True)

            return True
    # print(date, ts_code, False)
    return False


def get_gainian():
    pro = ts.pro_api('ee5c0e991e17949cdafbcf8ec42321ef4bac94e9ca3474e4d62313a3')
    path = './概念/'
    dir = Path(path)
    if not dir.exists():
        os.mkdir(dir)

    file = path + 'A概念.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pro.concept()
        df.to_csv(file, encoding='utf_8_sig')

    names = df['name'].values
    codes = df['code'].values
    for name, code in zip(names, codes):
        name = str.replace(name, '/', '')
        namefile = path + name + '.csv'
        if not os.path.exists(namefile):
            df = pro.concept_detail(id=code)
            df.to_csv(namefile, encoding='utf_8_sig')


def get_code_name(ts_code):
    markets = ['SSE', 'SZSE']
    for market in markets:
        if market == 'SSE':
            file = 'codes_SSE.csv'  # 生成大于指定收益的代码列表
            writefilename = 'sel_codes_SSE.csv'  # 在 大于指定收益的代码列表 中找到 当前ma5上扬的代码列表
            code_count = 1519  # 'SSE'
            all_codes_file = 'code_list_SSE.csv'
        else:
            file = 'codes_SZSE.csv'  # 生成大于指定收益的代码列表
            writefilename = 'sel_codes_SZSE.csv'  # 在 大于指定收益的代码列表 中找到 当前ma5上扬的代码列表
            code_count = 1417  # 'SZSE'
            all_codes_file = 'code_list_SZSE.csv'

        code_list = load_code_list(market=market)
        codes = code_list['ts_code'].values[:code_count]
        names = code_list['name'].values[:code_count]
        i = 0
        for code in codes:
            if code == ts_code:
                return names[i]
            else:
                i = i + 1
    print('NOName ************************** NoName')
    return 'noName'


def test(ts_code, name, days, begin_count, end_count, low_pct=-10, heigh_pct=30, isdebug=False, isCheckLow5=True):
    # print(ts_codes, 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    df = load_data(ts_code)

    # if end_count == 0:

    date = df['trade_date'].values
    close = df['close'].values
    change = df['change'].values
    pct_change = df['pct_chg'].values
    vol = df['vol'].values
    ma5 = df['ma5'].values
    ma10 = df['ma10'].values
    ma20 = df['ma20'].values
    ma30 = df['ma30'].values
    ma50 = df['ma50'].values
    ma120 = df['ma120'].values
    ma200 = df['ma200'].values

    ma_v_5 = df['ma_v_5'].values
    ma_v_10 = df['ma_v_10'].values
    ma_v_20 = df['ma_v_20'].values
    ma_v_30 = df['ma_v_30'].values
    ma_v_50 = df['ma_v_50'].values
    ma_v_120 = df['ma_v_120'].values

    price = 25
    if close.mean() < price:
        return -1, -1, -1, -1, -1

    index_array = np.array([])
    pct_array = np.array([])

    suc = 0
    fail = 0

    earnings = 0
    power = 0.0

    print(ts_code, name)
    # low_pct = -5
    # heigh_pct = 5
    # for i in range(begin_count+1, end_count):
    i = begin_count
    while i >= begin_count and i < end_count:
        i = i + 1
        if i >= end_count:
            break
        if i < len(pct_change) * -1 + 1:
            continue

        condition0 = close[i] > ma5[i]

        condition1 = ma5[i] > ma10[i]
        condition2 = ma10[i] < ma20[i]

        condition_0 = ma5[i] > ma5[i - 1]
        condition_1 = ma10[i] > ma10[i - 1]
        condition_2 = ma20[i] > ma20[i - 1]

        condition3 = ma20[i] > ma30[i]
        condition4 = ma30[i] > ma50[i]
        condition5 = ma50[i] > ma120[i]
        condition6 = ma120[i] > ma200[i]

        condition11 = ma_v_5[i] > ma_v_5[i - 1]
        condition12 = ma_v_5[i] > ma_v_10[i]
        condition13 = ma_v_5[i] > ma_v_20[i]
        condition14 = ma_v_10[i] > ma_v_30[i]
        condition15 = ma_v_20[i] > ma_v_50[i]
        condition16 = ma_v_50[i] > ma_v_120[i]

        conditionOne = pct_change[i] < 9.5
        conditionTwo = pct_change[i + 1] < 9.5

        if conditionOne and conditionTwo:  # pct_change[i+1] < 9.5  表示下一个交易日 涨停
            power = 1.2
            buys, sells = check_days_money(ts_code, name, date[i], days=5)
            if not buys / (sells + 1) > power:
                continue

            index_array = np.append(index_array, i)

            pct = 0
            for k in range(days):

                if (i + 1 + k) > -1:
                    break
                pct = pct + pct_change[i + 1 + k]
                if pct < low_pct:
                    pct = low_pct - 0.1
                    break
                elif pct > heigh_pct:
                    pct = heigh_pct
                    break

                out = 0.9

                # buys, sells = check_days_money(ts_code, name, date[i+1+k], days=5)
                # if buys / (sells + 1) < out:
                # break

                # if isCheckLow5:   # 检测是否低于10日均值
                #        if close[i+1+k] < ma10[i+1+k]:
                #            if isdebug:
                #                print("5555 ", 1+k, date[i+1+k], pct)
                # break
            if isdebug:
                print('DDDDDDDDDDDDDDDDD', i, close[i], date[i], pct)

            i = i + k
            if isdebug:
                print('PPPPPPPPPPPPPPPPP', i, close[i], date[i], pct)
            if pct > 0:
                suc = suc + 1
            else:
                fail = fail + 1

            pct_array = np.append(pct_array, pct)

            earnings = earnings + pct
    if isdebug:
        print('nnnnnnnnnnnnnnn', name)
        print('sssssssssssssss', suc)
        print('fffffffffffffff', fail)
        print('earnings ppppppppp', earnings)
        print(ts_code, 'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')

    return earnings, suc, fail, index_array, pct_array


def check_days_money(code, name, start_date='20160101', days=10):
    path = './All资金流向/'
    dir = Path(path)

    if not dir.exists():
        os.mkdir(dir)

    name = str.replace(name, '*', ' ')
    file = path + code + name + '.csv'
    if not os.path.exists(file):
        # 获取单日全部股票数据
        # print(code)
        try:
            df = pro.moneyflow(ts_code=code)
        except Exception:
            return 0, 0

        df.to_csv(file, encoding='utf_8_sig')

    df = pd.read_csv(file)
    # 去空
    df.dropna(inplace=True)
    # 正序
    df = df.sort_index(ascending=False)
    # 索引重排序
    df.reset_index(drop=True, inplace=True)

    dates = df['trade_date'].values

    codes = df['ts_code'].values
    buy_lg_vol = df['buy_lg_vol'].values
    sell_lg_vol = df['sell_lg_vol'].values
    buy_elg_vol = df['buy_elg_vol'].values
    sell_elg_vol = df['sell_elg_vol'].values
    # 日期对齐
    i = 0
    for date in dates:
        if date == start_date:
            break
        else:
            i = i + 1

    if i >= len(dates) or i <= days:
        return 0, 0
    # 日期对齐
    buys = 0
    sells = 0

    for k in range(days):
        # print(dates[i-k], code, buy_lg_vol[i-k], sell_lg_vol[i-k], buy_elg_vol[i-k], sell_elg_vol[i-k])
        buys = buys + buy_elg_vol[i - k] + buy_lg_vol[i - k]
        sells = sells + sell_elg_vol[i - k] + sell_lg_vol[i - k]

    return buys, sells


def get_dates_money(code, name):
    pro = ts.pro_api('ee5c0e991e17949cdafbcf8ec42321ef4bac94e9ca3474e4d62313a3')

    path = './All资金流向/'
    dir = Path(path)

    if not dir.exists():
        os.mkdir(dir)

    name = str.replace(name, '*', ' ')
    file = path + code + name + '.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        # 获取单日全部股票数据
        try:
            df = pro.moneyflow(ts_code=code)
            df.to_csv(file, encoding='utf_8_sig')
        except Exception:
            return None

    df = pd.read_csv(file)
    # 去空
    df.dropna(inplace=True)
    # 正序
    df = df.sort_index(ascending=False)
    # 索引重排序
    df.reset_index(drop=True, inplace=True)
    return df


def get_all_money(codes, names):
    pro = ts.pro_api('ee5c0e991e17949cdafbcf8ec42321ef4bac94e9ca3474e4d62313a3')

    path = './All资金流向/'
    dir = Path(path)

    if not dir.exists():
        os.mkdir(dir)
    for code, name in zip(codes, names):
        name = str.replace(name, '*', ' ')
        file = path + code + name + '.csv'
        if os.path.exists(file):
            df = pd.read_csv(file)
        else:
            try:
                df = pro.moneyflow(ts_code=code)
                df.to_csv(file, encoding='utf_8_sig')
            except Exception:
                continue


def get_perdata(trade_date, ts_code):
    pro = ts.pro_api('ee5c0e991e17949cdafbcf8ec42321ef4bac94e9ca3474e4d62313a3')

    path = './资金流向/'
    dir = Path(path)
    if not dir.exists():
        os.mkdir(dir)

    file = path + trade_date + '.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        # 获取单日全部股票数据
        df = pro.moneyflow(trade_date=trade_date)
        df.to_csv(file, encoding='utf_8_sig')

    codes = df['ts_code'].values
    buy_lg_vol = df['buy_lg_vol'].values
    sell_lg_vol = df['sell_lg_vol'].values
    buy_elg_vol = df['buy_elg_vol'].values
    sell_elg_vol = df['sell_elg_vol'].values
    i = 0
    for code in codes:
        if code == ts_code:
            break
        else:
            i = i + 1
    power = 1.5
    # print(trade_date, ts_code)
    if i >= len(buy_elg_vol):
        return False
    if (buy_elg_vol[i] + buy_lg_vol[i]) / (sell_elg_vol[i] + sell_lg_vol[i] + 1) > power:
        # print('predata True', trade_date, ts_code)
        # print(trade_date, ts_code, buy_lg_vol[i], sell_lg_vol[i], buy_elg_vol[i], sell_elg_vol[i])
        return True
    else:
        return False


def dividend(ts_code):
    df = pro.dividend(ts_code=ts_code)
    df.to_csv('dividend.csv', encoding='utf_8_sig')


def run():
    # market = 'SZSE'  # 交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
    markets = ['SSE', 'SZSE']

    for market in markets:

        if market == 'SSE':
            file = 'codes_SSE.csv'  # 生成大于指定收益的代码列表
            writefilename = 'sel_codes_SSE.csv'  # 在 大于指定收益的代码列表 中找到 当前ma5上扬的代码列表
            code_count = 1519  # 'SSE'
            all_codes_file = 'code_list_SSE.csv'
        else:
            file = 'codes_SZSE.csv'  # 生成大于指定收益的代码列表
            writefilename = 'sel_codes_SZSE.csv'  # 在 大于指定收益的代码列表 中找到 当前ma5上扬的代码列表
            code_count = 1417  # 'SZSE'
            all_codes_file = 'code_list_SZSE.csv'

        code_list = load_code_list(market=market)
        codes = code_list['ts_code'].values[:code_count]
        names = code_list['name'].values[:code_count]

        code = '601066.SH'

        begin_count = -600
        mid_count = -20
        end_count = -20
        days = 20

        testOne = 3

        if testOne == 1:
            name = get_code_name(code)
            earnings, suc, fail, index_array, pct_array = test(code, name, days=days, begin_count=begin_count,
                                                               end_count=end_count, isdebug=True)
            if suc == -1:
                return
            # draw_finance(code, begin_count=begin_count, end_count=end_count)

            path = './cur/'
            Dir = Path(path)
            if not Dir.exists():
                os.mkdir(Dir)

            if earnings > 0:
                file_dir = path + 'plt_%s++%.1f++%.1f.png' % (code, suc * 100 / (fail + suc + 1), earnings)
            else:
                file_dir = path + 'plt_%s--%.1f--%.1f.png' % (code, suc * 100 / (fail + suc + 1), earnings)

            plot_pct(code, index_array, pct_array, begin_count=begin_count, end_count=end_count, writefilename=file_dir)
            # cv2.imshow(file_dir)
            dividend(code)

        elif testOne == 2:
            all_test(codes, names=names, days=days, begin_count=begin_count, end_count=mid_count, writefile=file)
            test_sel_codes(days=days, names=names, begin_count=mid_count, end_count=end_count, file=file)

        elif testOne == 3:
            all_plot_pct(codes, names, days=days, begin_count=begin_count, end_count=end_count)
        elif testOne == 4:
            get_gainian()
        elif testOne == 5:
            get_all_money(codes, names)
        elif testOne == 6:
            all_sel_current_code(codes, names, writefileName=writefilename)


pro = ts.pro_api('62d436aa101ec224969e7d4f112414c29465a6753c275ea57786142d')
# market = 'SZSE'  # 交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
run()
