#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <algorithm>
#include <iomanip>
#include "DataHandler.h"
#include "Strategy.h"

using namespace std;

void exportTradeLog(const vector<TradeAction>& logs, const string& filename) {
    ofstream json(filename);
    json << "[\n";
    for (size_t i = 0; i < logs.size(); ++i) {
        json << "  {\"date\": \"" << logs[i].date 
             << "\", \"action\": \"" << logs[i].action 
             << "\", \"price\": " << logs[i].price 
             << ", \"shares\": " << logs[i].shares << "}";
        if (i < logs.size() - 1) json << ",\n";
    }
    json << "\n]";
    json.close();
}
// 這是 C++ 的函數，建議放在 main.cpp 的上方或獨立的 DataHandler.cpp 中
void exportToJSON(const vector<BarData>& data, const string& filename) {
    ofstream json(filename);
    if (!json.is_open()) return;

    json << "[\n";
    for (size_t i = 0; i < data.size(); ++i) {
        // 輸出 JSON 物件格式：{"date": "...", "price": ...}
        json << "  {\"date\": \"" << data[i].date << "\", \"price\": " << data[i].close << "}";
        if (i < data.size() - 1) json << ",\n"; // 最後一筆資料不加逗號
    }
    json << "\n]";
    json.close();
    cout << "✅ JSON 數據已成功匯出至: " << filename << endl;
}
int main(int argc, char* argv[]) {
    // 如果有傳入參數，就讀取該檔案；否則預設讀取 test.csv
    string inputFileName = (argc > 1) ? argv[1] : "test.csv";
    vector<TradeAction> myTradeLog;
    vector<BarData> myData = DataHandler::loadCSV(inputFileName);
    if (myData.empty()) return 1;

    MAStrategy myStrategy;
    double initialCash = 100000.0;
    double cash = initialCash;
    int holdings = 0;

    // --- 新增統計變數 ---
    double maxTotalValue = initialCash; 
    double maxDrawdown = 0.0;           // 最大回撤
    int totalTrades = 0;                // 總交易次數
    int winTrades = 0;                  // 獲利次數
    double entryPrice = 0.0;            // 記錄買入價格算勝率

    ofstream curveFile("equity_curve.csv");
    curveFile << "Date,Close,TotalValue,Cash,Holdings\n";

    cout << "--- Starting Backtest: Moving Average Strategy ---" << endl;

    for (const auto& bar : myData) {
        myStrategy.onBar(bar);
        int signal = myStrategy.getSignal();

        // 買入邏輯
        if (signal == 1 && holdings == 0) {
            holdings = cash / bar.close;
            cash -= holdings * bar.close;
            entryPrice = bar.close; // 紀錄買入價
            totalTrades++;
            myTradeLog.push_back({bar.date, "BUY", bar.close, holdings});
            cout << "BUY  | " << bar.date << " | Price: " << bar.close << endl;
        } 
        // 賣出邏輯
        else if (signal == -1 && holdings > 0) {
            if (bar.close > entryPrice) winTrades++; // 賣出比買入高就是贏
            cash += holdings * bar.close;
            myTradeLog.push_back({bar.date, "SELL", bar.close, 0});
            cout << "SELL | " << bar.date << " | Price: " << bar.close << endl;
            holdings = 0;
        }
        // 計算當日淨值並記錄
        double currentTotalValue = cash + (holdings * bar.close);
        maxTotalValue = max(maxTotalValue, currentTotalValue);
        double currentDrawdown = (maxTotalValue - currentTotalValue) / maxTotalValue;
        maxDrawdown = max(maxDrawdown, currentDrawdown);

        // 寫入 CSV 供後續繪圖
        curveFile << bar.date << "," << bar.close << "," << currentTotalValue << "," 
                  << cash << "," << holdings << "\n";
    }
    curveFile.close();

    // 最後結算
    double finalValue = cash + (holdings * myData.back().close);
    double totalReturn = ((finalValue - initialCash) / initialCash) * 100;
    double winRate = (totalTrades > 0) ? (double)winTrades / (totalTrades) * 100 : 0;

    cout << "\n===========================================" << endl;
    cout << "Backtest Completed!" << endl;
    cout << "Final Portfolio Value : $" << fixed << setprecision(2) << finalValue << endl;
    cout << "Total Return Rate     : " << totalReturn << "%" << endl;
    cout << "Win Rate              : " << winRate << "% (" << winTrades << "/" << totalTrades << ")" << endl;
    cout << "Max Drawdown (MDD)    : " << maxDrawdown * 100 << "%" << endl;
    cout << "Results saved to: equity_curve.csv" << endl;
    cout << "===========================================" << endl;

    // 匯出 JSON 數據供前端使用
    exportToJSON(myData, "data.json");
    exportTradeLog(myTradeLog, "trade_log.json");
    return 0;
}