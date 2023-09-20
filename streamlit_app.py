import streamlit as st
import pandas as pd
from datetime import datetime
from datetime import  timedelta
from app.main.Main import Main

# ==================== 定義預設值 ====================

today = datetime.today()
default_end_date = today.strftime('%Y-%m-%d')
default_start_date = (today - timedelta(days=3*365)).strftime('%Y-%m-%d')
is_fund = False
using_taiwan_stock_crawl = False
using_taiwan_etf_crawl = False
using_yf = False
consider_tax = False

# ==================== 標題 ====================

st.title('股票定期定額模擬器💵')
st.caption('股票定期定額回測的模擬器。')
st.caption('*~~早知當初... 都有定期定額買，現在會怎麼樣🥲~~*')
st.caption('免責聲明：這只是個投資試算工具，僅供參考')

# ==================== 基本設定 ====================

st.subheader('基本設定', divider=True)
mode_str = st.radio(
    "選擇類型",
    [
        "台股",
        '自行填寫代號(台股)',
        "美股",
        '自行填寫代號(美股)',
        '~~台灣基金 (施工中🚧)~~',
        '~~VWRA (施工中🚧)~~',
    ])
start_date = st.text_input("開始時間", default_start_date)
end_date = st.text_input("結束時間", default_end_date)

investment_amount = st.number_input('每次定期定額投資金額', value=10000)
purchase_day = st.number_input('每月第 N 個交易天進行交易', value=1)

# ==================== 選擇股票 ====================

st.subheader('選擇股票', divider=True)

if mode_str == '台股':
    code = st.selectbox(
        '選擇代號',
        (
            '0050',
            '0056',
            '2330-台積電',
            '2881-富邦金',
            '2882-國泰金',
            '2884-玉山金',
            '2887-台新金',
            '5880-合庫金',
            '9941-裕融',
            '2480-敦陽科',
            '2618-長榮航空',
        )
    )
    code = code.split('-')[0]
    code = code + '.TW'
    using_taiwan_stock_crawl = True
    using_taiwan_etf_crawl = False
    # using_taiwan_stock_crawl = st.checkbox('使用台股爬蟲(goodinfo.tw)？', True)
    # using_taiwan_etf_crawl = st.checkbox('使用台股ETF爬蟲(www.moneydj.com)？', False)

if mode_str == '自行填寫代號(台股)':
    code = st.text_input("自行填寫代號(台股)")
    code = code + '.TW'
    using_taiwan_stock_crawl = True
    using_taiwan_etf_crawl = False
    # using_taiwan_stock_crawl = st.checkbox('使用台股爬蟲(goodinfo.tw)？', True)
    # using_taiwan_etf_crawl = st.checkbox('使用台股ETF爬蟲(www.moneydj.com)？', False)

if mode_str == '台灣基金':
    code = st.selectbox(
        '選擇代號',
        (
            'ACDD01-安聯台灣大壩基金A累積型(台幣)'
        )
    )
    code = code.split('-')[0]
    is_fund = True

if mode_str == 'VWRA':
    code = 'VWRA.L'
    using_yf = True

if mode_str == '美股':
    code = st.selectbox(
        '選擇代號',
        (
            'VT',
            'VTI',
            'SPY',
            'AAPL',
            'NVDA',
            'TSLA',
        )
    )
    using_yf = True
    consider_tax = st.checkbox('考量到美股股息稅(30%)？', True)

if mode_str == '自行填寫代號(美股)':
    code = st.text_input("自行填寫代號(美股)")
    using_yf = True
    consider_tax = st.checkbox('考量到美股股息稅(30%)？', True)

# ==================== 開始試算 ====================
if st.button('開始試算'):

    app = Main()
    app.code = code # 股票代碼
    app.start_date = start_date # 起始日期
    app.end_date = end_date # 結束日期
    app.investment_amount = investment_amount
    app.purchase_day = purchase_day
    app.is_fund = is_fund
    app.using_taiwan_stock_crawl = using_taiwan_stock_crawl
    app.using_taiwan_etf_crawl = using_taiwan_etf_crawl
    app.using_yf = using_yf
    app.consider_tax = consider_tax

    result_dict = app.launch()
    result_summary_str = result_dict['result_summary_str']
    trade_record_df = result_dict['trade_record_df']
    value_record_df = result_dict['value_record_df']

    st.write("試算結果: ")
    st.text(result_summary_str)

    st.write("股票價值成長折線圖: ")
    chart_df = pd.DataFrame({
        '股票價值': value_record_df["total_value"],
        '股票成本': value_record_df["total_cost"],
        '股票成本(扣除股息)': value_record_df["total_cost_with_dividend"],
    })
    st.line_chart(chart_df)

    st.write("投資損益成長折線圖: ")
    chart_data = pd.DataFrame({
        '數字零位置': [ 0 for _ in range(value_record_df.index.size)],
        '投資損益': value_record_df["profit_rate"],
        '投資損益(含股息)': value_record_df["profit_rate_with_dividend"],
    })
    st.line_chart(chart_data)

    st.write("成交紀錄: ")
    st.dataframe(trade_record_df)

    st.write("歷史價值: ")
    st.dataframe(value_record_df)

# st.subheader('TODO', divider=True)
# st.text('1. 說明方式計算。')
# st.text('2. 確認台股股價，似乎在股票股息計算價格會有問題。')
