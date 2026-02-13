import streamlit as st
import subprocess
import pandas as pd
import json
import os

# --- 新增：Python 版備援策略 (均線邏輯與 C++ 一致) ---
def run_python_fallback(df):
    df = df.copy()
    # 確保 Close 欄位是數值
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['MA5'] = df['Close'].rolling(window=5).mean()
    
    cash = 100000.0
    holdings = 0
    trade_logs = []
    equity_curve = []
    
    for i in range(len(df)):
        price = df.iloc[i]['Close']
        date = df.index[i].strftime('%Y-%m-%d') if hasattr(df.index[i], 'strftime') else str(df.index[i])
        ma5 = df.iloc[i]['MA5']
        
        if not pd.isna(ma5):
            if price > ma5 and holdings == 0:  # 買入
                holdings = int(cash // price)
                cash -= holdings * price
                trade_logs.append({"date": date, "action": "BUY", "price": float(price), "shares": int(holdings)})
            elif price < ma5 and holdings > 0: # 賣出
                cash += holdings * price
                trade_logs.append({"date": date, "action": "SELL", "price": float(price), "shares": 0})
                holdings = 0
        
        total_value = cash + (holdings * price)
        equity_curve.append({"date": date, "price": float(total_value)})
        
    return equity_curve, trade_logs

# --- Streamlit 介面 ---
st.title("🚀 量化交易策略回測平台 (雲端相容版)")

uploaded_file = st.file_uploader("選擇股票數據 CSV 檔案", type=["csv"])

if uploaded_file is not None:
    # 讀取數據
    df_input = pd.read_csv(uploaded_file, index_col=0, parse_dates=True)
    st.success(f"已載入檔案: {uploaded_file.name}")
    
    # 暫存一份給 C++ 讀取（僅限本地環境）
    df_input.to_csv("temp_input.csv")

    if st.button("開始分析"):
        with st.spinner('引擎運算中...'):
            try:
                # 嘗試執行 C++ (本地 Windows 環境會成功)
                result = subprocess.run(["./BacktestApp", "temp_input.csv"], capture_output=True, check=True)
                
                # 讀取 C++ 產出的 JSON
                with open("data.json", "r") as f: plot_data = json.load(f)
                with open("trade_log.json", "r") as f: trades = json.load(f)
                st.info("✅ 已調用本地 C++ 高效能引擎")
                
            except (FileNotFoundError, subprocess.CalledProcessError, OSError):
                # 雲端 Linux 環境執行失敗時，自動觸發 Python 備援
                st.warning("⚠️ 偵測到雲端 Linux 環境，自動切換至 Python 備援引擎")
                plot_data, trades = run_python_fallback(df_input)

            # --- 顯示結果 (無論是 C++ 或 Python 產出，格式都一樣) ---
            st.subheader("📈 淨值曲線圖")
            st.line_chart(pd.DataFrame(plot_data).set_index('date'))
            
            st.subheader("🔔 交易執行日誌")
            for t in trades:
                icon = "📥" if t['action'] == "BUY" else "📤"
                st.markdown(f"{icon} **{t['date']}** ：以 `${t['price']:.2f}` **{t['action']}** -> 持有：`{t['shares']}` 股")