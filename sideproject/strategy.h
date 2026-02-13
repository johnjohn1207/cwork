#ifndef STRATEGY_H
#define STRATEGY_H

#include "DataHandler.h"
#include <vector>
#include <string>
#include <deque>
#include <numeric> // 為了使用 std::accumulate

// 1. 基類
class Strategy {
public:
    virtual ~Strategy() {}
    virtual void onBar(const BarData& bar) = 0;
    virtual int getSignal() = 0;
};

// 2. 均線策略
class MAStrategy : public Strategy {
private:
    int signal = 0;
    std::deque<double> priceWindow; 
    const int windowSize = 5;

public:
    void onBar(const BarData& bar) override {
        priceWindow.push_back(bar.close);
        if (priceWindow.size() > (size_t)windowSize) {
            priceWindow.pop_front();
        }

        if (priceWindow.size() == (size_t)windowSize) {
            double sum = std::accumulate(priceWindow.begin(), priceWindow.end(), 0.0);
            double ma5 = sum / windowSize;

            if (bar.close > ma5) {
                signal = 1;
            } else {
                signal = -1;
            }
        } else {
            signal = 0;
        }
    }

    int getSignal() override { return signal; }
};

// 3. 交易紀錄結構
// 修正：在標頭檔中，請使用 std::string 以避免編譯錯誤
struct TradeAction {
    std::string date;
    std::string action; // "BUY" 或 "SELL"
    double price;
    int shares;
};

#endif