#include <iostream>
#include <new>     // std::nothrow
#include <cstddef>
using namespace std;

float* allocateAltitudeData(unsigned int seconds)
{
    if (seconds == 0) return nullptr;
    return new (std::nothrow) float[seconds];
}

float* findMaxAltitude(float* data, unsigned int size)
{
    if (data == nullptr || size == 0) return nullptr;

    float* maxPtr = data;
    float* p = data + 1;
    float* end = data + size;

    while (p < end) {
        if (*p > *maxPtr) maxPtr = p;
        ++p;
    }
    return maxPtr;
}

float* findMinAltitude(float* data, unsigned int size)
{
    if (data == nullptr || size == 0) return nullptr;

    float* minPtr = data;
    float* p = data + 1;
    float* end = data + size;

    while (p < end) {
        if (*p < *minPtr) minPtr = p;
        ++p;
    }
    return minPtr;
}

float* calculateAverageAltitude(float* data, unsigned int size)
{
    if (data == nullptr || size == 0) return nullptr;

    double sum = 0.0;
    float* p = data;
    float* end = data + size;

    while (p < end) {
        sum += *p;
        ++p;
    }

    float* avgPtr = new (std::nothrow) float;
    if (!avgPtr) return nullptr;

    *avgPtr = static_cast<float>(sum / size);
    return avgPtr;
}

void freeMemory(float* ptr, bool isArray)
{
    if (ptr == nullptr) return;

    if (isArray) delete[] ptr;
    else delete ptr;
}

int main()
{
    unsigned int seconds;

    cout << "Enter flight duration (seconds): ";
    cin >> seconds;

    // 1️⃣ 配置記憶體
    float* altitudeData = allocateAltitudeData(seconds);

    if (altitudeData == nullptr) {
        cout << "Memory allocation failed.\n";
        return 1;
    }

    // 2️⃣ 讀取高度資料
    cout << "Enter altitude readings:\n";
    for (unsigned int i = 0; i < seconds; i++) {
        cout << "Second " << i << ": ";
        cin >> altitudeData[i];
    }

    // 3️⃣ 找最大值（回傳指標）
    float* maxPtr = findMaxAltitude(altitudeData, seconds);

    // 4️⃣ 找最小值（回傳指標）
    float* minPtr = findMinAltitude(altitudeData, seconds);

    // 5️⃣ 算平均（回傳 new 出來的 float*）
    float* avgPtr = calculateAverageAltitude(altitudeData, seconds);

    // 6️⃣ 顯示結果（注意全部都從指標解參考）
    cout << "\n===== Flight Report =====\n";

    if (maxPtr) cout << "Maximum altitude: " << *maxPtr << endl;
    if (minPtr) cout << "Minimum altitude: " << *minPtr << endl;
    if (avgPtr) cout << "Average altitude: " << *avgPtr << endl;

    // 7️⃣ 釋放記憶體（非常重要）
    freeMemory(altitudeData, true);   // 陣列
    freeMemory(avgPtr, false);        // 單一 float

    return 0;
}