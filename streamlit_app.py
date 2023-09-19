import streamlit as st
import pandas as pd
from app.main.Main import Main


text_select = st.selectbox(
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
            'VWRA.L',
            'VT',
            'ACDD01-安聯台灣大壩基金A累積型(台幣)'
        )
    )
text_input = st.text_input("找不到？試試自行填寫代號")
is_tw_stock = st.checkbox('是否為台股？', True)
start_date = st.text_input("開始時間", "2022-01-01")
end_date = st.text_input("結束時間", "2023-06-18")
investment_amount = st.number_input('每次定期定額投資金額', value=10000)
purchase_day = st.number_input('每月第 N 個交易天進行交易', value=1)
is_fund = st.checkbox('是否為基金？', False)
using_taiwan_stock_crawl = st.checkbox('使用台股爬蟲(goodinfo.tw)？', True)
using_taiwan_etf_crawl = st.checkbox('使用台股ETF爬蟲(www.moneydj.com)？', False)

if st.button('開始試算'):
    if text_input:
        code = text_input
    if text_select:
        code = text_select
    code = code.split('-')[0]
    if is_tw_stock:
        code = code + '.TW'
    st.write("使用代號: ", code)

    app = Main()
    app.code = code # 股票代碼
    app.start_date = start_date # 起始日期
    app.end_date = end_date # 結束日期
    app.investment_amount = investment_amount
    app.purchase_day = purchase_day
    app.is_fund = is_fund
    app.using_taiwan_stock_crawl = using_taiwan_stock_crawl
    app.using_taiwan_etf_crawl = using_taiwan_etf_crawl

    result_dict = app.launch()
    result_summary_str = result_dict['result_summary_str']
    trade_record_df = result_dict['trade_record_df']
    value_record_df = result_dict['value_record_df']

    st.write("試算結果: ")
    st.text(result_summary_str)
    st.write("歷史成交模擬: ")
    st.dataframe(trade_record_df)
    st.write("歷史價值模擬: ")
    st.dataframe(value_record_df)
