import streamlit as st
import subprocess
import pandas as pd
import json
import os
import yfinance as yf

# --- 1. 配置頁面樣式 ---
st.set_page_config(page_title="量化交易回測平台", page_icon="📈", layout="wide")

# --- 2. Python 版備援策略 (加入統計計算邏輯) ---
def run_python_fallback(df):
    df = df.copy()
    
    # 處理 Yahoo Finance 的多重索引
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    close_series = df['Close'].iloc[:, 0] if isinstance(df['Close'], pd.DataFrame) else df['Close']
    df['Close'] = pd.to_numeric(close_series, errors='coerce')
    df['MA5'] = df['Close'].rolling(window=5).mean()
    
    initial_cash = 100000.0
    cash, holdings, trade_logs, equity_curve = initial_cash, 0, [], []
    win_trades, total_trades, entry_price = 0, 0, 0.0  # 新增統計變數

    for i in range(len(df)):
        price = float(df.iloc[i]['Close'])
        date_str = df.index[i].strftime('%Y-%m-%d') if hasattr(df.index[i], 'strftime') else str(df.index[i])
        ma5 = df.iloc[i]['MA5']
        
        if not pd.isna(ma5):
            if price > ma5 and holdings == 0:  # 買入
                holdings = int(cash // price)
                cash -= holdings * price
                entry_price = price  # 紀錄進場價
                total_trades += 1
                trade_logs.append({"date": date_str, "action": "BUY", "price": price, "shares": holdings})
            elif price < ma5 and holdings > 0: # 賣出
                if price > entry_price: win_trades += 1 # 判斷是否獲利
                cash += holdings * price
                trade_logs.append({"date": date_str, "action": "SELL", "price": price, "shares": 0})
                holdings = 0
        
        equity_curve.append({"date": date_str, "price": cash + (holdings * price)})

    # 計算統計指標
    final_val = equity_curve[-1]['price']
    metrics = {
        "final_value": final_val,
        "total_return": ((final_val - initial_cash) / initial_cash) * 100,
        "win_rate": (win_trades / total_trades * 100) if total_trades > 0 else 0
    }
    
    return equity_curve, trade_logs, metrics

# --- 3. 核心分析與顯示函數 ---
def perform_backtest_analysis(df_input):
    df_input.to_csv("temp_input.csv")
    
    with st.spinner('🚀 運算引擎分析中...'):
        try:
            # 優先嘗試執行 C++
            subprocess.run(["./BacktestApp", "temp_input.csv"], capture_output=True, check=True)
            with open("data.json", "r", encoding="utf-8") as f: plot_data = json.load(f)
            with open("trade_log.json", "r", encoding="utf-8") as f: trades = json.load(f)
            
            # 即使是 C++ 跑完，我們也用 Python 快速算一下指標卡片
            _, _, metrics = run_python_fallback(df_input)
            st.info("⚡ 系統訊息：已成功調用本地 C++ 高效能運算引擎。")
            
        except (FileNotFoundError, subprocess.CalledProcessError, OSError):
            st.warning("🌐 雲端環境偵測：已自動切換至 Python 跨平台相容引擎。")
            plot_data, trades, metrics = run_python_fallback(df_input)

    # --- 頂部統計指標卡片區塊 ---
    m1, m2, m3 = st.columns(3)
    m1.metric("最終資產淨值", f"${metrics['final_value']:,.2f}")
    m2.metric("總報酬率", f"{metrics['total_return']:.2f}%")
    m3.metric("策略勝率", f"{metrics['win_rate']:.2f}%")

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

# --- 4. Streamlit 介面佈局 (保持不變) ---
st.title("🚀 全自動量化交易回測系統")
st.sidebar.header("📡 數據自動獲取")
ticker = st.sidebar.text_input("輸入股票代碼 (例: NVDA, 2330.TW)", value="2330.TW")
start_d = st.sidebar.date_input("開始日期", value=pd.to_datetime("2024-01-01"))
end_d = st.sidebar.date_input("結束日期", value=pd.to_datetime("2026-02-13"))

if st.sidebar.button("獲取最新數據並回測"):
    with st.spinner(f'正在串接 Yahoo Finance API 下載 {ticker}...'):
        df_api = yf.download(ticker, start=start_d, end=end_d)
        if not df_api.empty:
            if isinstance(df_api.columns, pd.MultiIndex):
                df_api.columns = df_api.columns.get_level_values(0)
            df_api = df_api[['Open', 'High', 'Low', 'Close', 'Volume']]
            st.sidebar.success(f"✅ {ticker} 數據獲取成功！")
            perform_backtest_analysis(df_api)
        else:
            st.sidebar.error("數據抓取失敗。")

st.markdown("---")
st.subheader("📁 手動模式：上傳歷史 CSV")
uploaded_file = st.file_uploader("若您已有整理好的 CSV 檔案，請在此上傳", type=["csv"])

if uploaded_file is not None:
    df_upload = pd.read_csv(uploaded_file, index_col=0, parse_dates=True)
    st.success(f"成功載入檔案：{uploaded_file.name}")
    if st.button("執行上傳檔案回測"):
        perform_backtest_analysis(df_upload)