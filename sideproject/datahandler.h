#ifndef DATAHANDLER_H
#define DATAHANDLER_H

#include <vector>
#include <string>

// 移除這裡的 using namespace std;

// 定義每一根 K 線的結構
struct BarData {
    std::string date;
    double open;
    double high;
    double low;
    double close;
    long long volume;
};

// 負責處理資料讀取的類別
class DataHandler {
public:
    // 在宣告時明確寫出 std::vector 和 std::string
    static std::vector<BarData> loadCSV(std::string filename);
};

#endif