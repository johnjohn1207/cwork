import streamlit as st
import subprocess
import pandas as pd
import json
import os
import yfinance as yf

# --- 1. 配置頁面樣式 ---
st.set_page_config(page_title="量化交易回測平台", page_icon="📈", layout="wide")

# --- 2. Python 版備援策略 (確保雲端環境服務不中斷) ---
def run_python_fallback(df):
    df = df.copy()
    
    # --- 關鍵修正：處理 Yahoo Finance 的多重索引格式 ---
    if isinstance(df.columns, pd.MultiIndex):
        # 降維：只保留第一層索引 (Open, Close 等)
        df.columns = df.columns.get_level_values(0)
    
    # 確保 Close 欄位是單一的 Series 而非 DataFrame
    if isinstance(df['Close'], pd.DataFrame):
        close_series = df['Close'].iloc[:, 0]
    else:
        close_series = df['Close']
        
    df['Close'] = pd.to_numeric(close_series, errors='coerce')
    # 確保 Close 欄位是數值型態，避免 API 抓取的格式問題
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['MA5'] = df['Close'].rolling(window=5).mean()
    
    cash = 100000.0
    holdings = 0
    trade_logs = []
    equity_curve = []
    
    for i in range(len(df)):
        price = df.iloc[i]['Close']
        # 處理日期格式
        if hasattr(df.index[i], 'strftime'):
            date_str = df.index[i].strftime('%Y-%m-%d')
        else:
            date_str = str(df.index[i])
            
        ma5 = df.iloc[i]['MA5']
        
        if not pd.isna(ma5):
            # 策略：收盤價突破 MA5 買入，跌破 MA5 賣出
            if price > ma5 and holdings == 0:
                holdings = int(cash // price)
                cash -= holdings * price
                trade_logs.append({"date": date_str, "action": "BUY", "price": float(price), "shares": int(holdings)})
            elif price < ma5 and holdings > 0:
                cash += holdings * price
                trade_logs.append({"date": date_str, "action": "SELL", "price": float(price), "shares": 0})
                holdings = 0
        
        # 計算每日總資產 (現金 + 持股市值)
        total_value = cash + (holdings * price)
        equity_curve.append({"date": date_str, "price": float(total_value)})
        
    return equity_curve, trade_logs

# --- 3. 核心分析與顯示函數 ---
def perform_backtest_analysis(df_input):
    """
    封裝分析邏輯，支援 C++ 優先與 Python 備援。
    """
    # 統一儲存為 C++ 引擎可讀取的格式
    df_input.to_csv("temp_input.csv")
    
    with st.spinner('🚀 運算引擎分析中...'):
        try:
            # 優先嘗試執行本地編譯的 C++ 執行檔
            # check=True 會在執行失敗時拋出異常，觸發 except 區塊
            subprocess.run(["./BacktestApp", "temp_input.csv"], capture_output=True, check=True)
            
            # 讀取 C++ 產出的數據結果
            with open("data.json", "r", encoding="utf-8") as f: plot_data = json.load(f)
            with open("trade_log.json", "r", encoding="utf-8") as f: trades = json.load(f)
            st.info("⚡ 系統訊息：已成功調用本地 C++ 高效能運算引擎。")
            
        except (FileNotFoundError, subprocess.CalledProcessError, OSError):
            # 若為雲端 Linux 環境，自動執行 Python 備援邏輯
            st.warning("🌐 雲端環境偵測：已自動切換至 Python 跨平台相容引擎。")
            plot_data, trades = run_python_fallback(df_input)

    # --- 視覺化呈現區塊 ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 策略資產淨值曲線")
        chart_df = pd.DataFrame(plot_data).set_index('date')
        st.line_chart(chart_df)
        
    with col2:
        st.subheader("🔔 交易執行明細")
        if trades:
            for t in trades:
                color = "green" if t['action'] == "BUY" else "red"
                icon = "📥" if t['action'] == "BUY" else "📤"
                st.markdown(f"{icon} **{t['date']}** : <span style='color:{color}'>{t['action']}</span> @ **${t['price']:.2f}** (持有: {t['shares']} 股)", unsafe_allow_html=True)
        else:
            st.write("目前區間內無交易訊號產生。")

# --- 4. Streamlit 介面佈局 ---
st.title("🚀 全自動量化交易回測系統")
st.markdown("本系統整合了 **Yahoo Finance API**、**C++ 核心運算** 與 **Python 數據視覺化**。")

# 側邊欄：自動化數據獲取
st.sidebar.header("📡 數據自動獲取")
ticker = st.sidebar.text_input("輸入股票代碼 (例: NVDA, 2330.TW)", value="2330.TW")
start_d = st.sidebar.date_input("開始日期", value=pd.to_datetime("2024-01-01"))
end_d = st.sidebar.date_input("結束日期", value=pd.to_datetime("2026-02-13"))

if st.sidebar.button("獲取最新數據並回測"):
    with st.spinner(f'正在串接 Yahoo Finance API 下載 {ticker}...'):
        df_api = yf.download(ticker, start=start_d, end=end_d)
        if not df_api.empty:
            # 資料清洗：移除多餘索引並確保格式
            df_api = df_api[['Open', 'High', 'Low', 'Close', 'Volume']]
            st.sidebar.success(f"✅ {ticker} 數據獲取成功！")
            perform_backtest_analysis(df_api)
        else:
            st.sidebar.error("數據抓取失敗，請檢查代碼或日期設定。")

# 主頁面：手動上傳區塊
st.markdown("---")
st.subheader("📁 手動模式：上傳歷史 CSV")
uploaded_file = st.file_uploader("若您已有整理好的 CSV 檔案，請在此上傳", type=["csv"])

if uploaded_file is not None:
    df_upload = pd.read_csv(uploaded_file, index_col=0, parse_dates=True)
    st.success(f"成功載入檔案：{uploaded_file.name}")
    if st.button("執行上傳檔案回測"):
        perform_backtest_analysis(df_upload)