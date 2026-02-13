#include "DataHandler.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>  // 建議明確加上這個，確保 vector 被定義

using namespace std;

// 確保你的 DataHandler.h 裡面 BarData 也是定義在全域或正確的 namespace 下
vector<BarData> DataHandler::loadCSV(string filename) {
    vector<BarData> data;
    ifstream file(filename);

    if (!file.is_open()) {
        cerr << "無法開啟檔案: " << filename << endl;
        return data;
    }

    string line;
    // 檢查是否有第一行可以跳過
    getline(file, line); // 跳過第一行 (Price/Ticker...)
    getline(file, line); // 跳過第二行 (NVDA/NVDA...)
    getline(file, line); // 跳過第三行 (Date/Open...

    while (getline(file, line)) {
        if (line.empty()) continue; // 防呆：跳過空白行
        
        stringstream ss(line);
        BarData bar;
        string temp;

        try {
            // 解析逗號隔開的每一項
            getline(ss, bar.date, ',');
            getline(ss, temp, ','); bar.open = stod(temp);
            getline(ss, temp, ','); bar.high = stod(temp);
            getline(ss, temp, ','); bar.low = stod(temp);
            getline(ss, temp, ','); bar.close = stod(temp);
            getline(ss, temp, ','); bar.volume = stoll(temp);

            data.push_back(bar);
        } catch (...) {
            // 如果 CSV 格式有誤（例如某行資料缺損），跳過該行而不讓程式崩潰
            continue; 
        }
    }

    file.close();
    return data;
}