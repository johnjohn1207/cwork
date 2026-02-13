import yfinance as yf

# 設定你想下載的股號 (台股要加 .TW)
# ticker = "2330.TW"  # 台積電
ticker = "2330.TW"     # 輝達

print(f"正在從 Yahoo Finance 下載 {ticker} 的數據...")

# 下載過去一年的日 K 線資料
data = yf.download(ticker, start="2025-01-01", end="2026-02-13")

# 格式調整：確保欄位是你 C++ DataHandler 認得的 Date, Open, High, Low, Close, Volume
# yfinance 下載下來的 Date 會是 Index，轉成 CSV 時會自動變成第一欄
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
filename = f"{ticker}_data.csv"
# 存成 test.csv
data.to_csv(filename, index=True)

print(f"下載完成！檔案已存為 {filename}")
