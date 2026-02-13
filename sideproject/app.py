import streamlit as st
import subprocess
import pandas as pd
import json
import os

st.title("🚀 量化交易策略回測平台")

uploaded_file = st.file_uploader("選擇你的股票數據 CSV 檔案", type=["csv"])

if uploaded_file is not None:
    with open("temp_input.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"已載入檔案: {uploaded_file.name}")

if st.button("開始分析"):
    with st.spinner('C++ 引擎正在運算中...'):
        result = subprocess.run(["./BacktestApp", "temp_input.csv"], capture_output=True, check=False)
        
        if result.returncode == 0:
            st.balloons()
            
            # 1. 顯示圖表
            if os.path.exists("data.json"):
                with open("data.json", "r", encoding="utf-8") as f:
                    plot_data = json.load(f)
                df_plot = pd.DataFrame(plot_data)
                st.subheader("📈 淨值曲線圖")
                st.line_chart(df_plot.set_index('date'))
            
            # 2. 【核心修正】顯示文字交易日誌：放在按鈕成功的區塊內
            if os.path.exists("trade_log.json"):
                with open("trade_log.json", "r", encoding="utf-8") as f:
                    trades = json.load(f)
                
                st.subheader("🔔 交易執行日誌")
                for t in trades:
                    icon = "📥" if t['action'] == "BUY" else "📤"
                    st.markdown(f"{icon} **{t['date']}** ：以價格 `{t['price']:.2f}` **{t['action']}** -> 當前持股數量：`{t['shares']}` 股")

            # 3. 顯示詳細明細表
            if os.path.exists("equity_curve.csv"):
                df_detail = pd.read_csv("equity_curve.csv")
                st.subheader("📋 交易明細")
                st.dataframe(df_detail)
        else:
            st.error("C++ 引擎執行失敗。")