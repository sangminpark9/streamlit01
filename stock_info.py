import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import datetime
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import plotly.graph_objects as go
import pandas as pd
from io import BytesIO

st.title('무슨 주식을 사야 부자가 되려나')

with st.sidebar:
    st.title('회사 이름과 기간을 입력하세요')
    stock_name = st.text_input('회사이름')
    today = datetime.date.today()
    # 날짜 범위 입력 위젯 생성
    start_date, end_date = st.date_input(
        'Select a date range',
        value=(today, today + datetime.timedelta(days=7)))
    button_result = st.button('주가데이터 확인')
date_range=[]
date_range.append(start_date)
date_range.append(end_date)

@st.cache_data
def get_stock_info():
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"
    method = "download"
    url = "{0}?method={1}".format(base_url, method)
    df = pd.read_html(url, header=0,encoding='euc-kr')[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")
    df = df[['회사명','종목코드']]
    return df

def get_ticker_symbol(company_name):
    df = get_stock_info()
    code = df[df['회사명']==company_name]['종목코드'].values
    ticker_symbol = code[0]
    return ticker_symbol
# 코드 조각 추가
if button_result:
    ticker_symbol = get_ticker_symbol(stock_name)
    if ticker_symbol:
        start_p = date_range[0]
        end_p = date_range[1] + datetime.timedelta(days=1)
        df = fdr.DataReader(f'KRX:{ticker_symbol}', start_p, end_p)
        df = df.iloc[:, :6]
        df.index = df.index.date
        
        st.subheader(f"[{stock_name}] 주가 데이터")
        st.dataframe(df.tail(7))
        st.line_chart(df.Close)
        
        excel_data = BytesIO()
        csv_data = BytesIO()
        
        col1, col2 = st.columns(2)

        df.to_csv(csv_data)
        csv_data.seek(0)  # 포지션 재설정
        df.to_excel(excel_data)
        csv_data.seek(0)  # 포지션 재설정
        with col1:
            st.download_button("CSV 파일 다운로드",
                            csv_data, file_name='sotck_data.csv')
        with col2:    
            st.download_button("엑셀 파일 다운로드",
                    excel_data, file_name='stock_data.xlsx')
else :
    st.error("유효하지 않은 회사 이름입니다. 다시 입력해주세요.")