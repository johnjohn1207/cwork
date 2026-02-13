# 1. 定義變數
CXX = g++
CXXFLAGS = -std=c++11 -O3 -Wall
TARGET = BacktestApp
SRCS = main.cpp DataHandler.cpp

# 2. 預設動作 (打 make 就執行這行)
# 這會把原始碼編譯成執行檔
all:
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

# 3. 執行動作 (打 make run 就會編譯並自動執行)
run: all
	./$(TARGET)

# 4. 清除動作 (打 make clean 會把執行檔刪掉，重新開始)
clean:
	rm -f $(TARGET)