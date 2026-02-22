#include <iostream>
#include <string>

using namespace std;

// 1) 定義 struct
struct Patient {
    string name;
    int age;
    string condition;
};

// 2) 新增病患
void addPatient(Patient*& patients,
                unsigned int& count,
                const string& name,
                unsigned int age,
                const string& condition)
{
    // 開一個更大的新陣列
    Patient* newPatients = new Patient[count + 1];

    // 複製舊資料
    for (unsigned int i = 0; i < count; i++) {
        newPatients[i] = patients[i];
    }

    // 加入新病患
    newPatients[count].name = name;
    newPatients[count].age = age;
    newPatients[count].condition = condition;

    // 刪除舊記憶體
    delete[] patients;

    // 更新指標
    patients = newPatients;

    // 數量增加
    count++;
}

// 3) 移除病患
void removePatient(Patient*& patients,
                   unsigned int& count,
                   unsigned int index)
{
    // 檢查 index
    if (index >= count) {
        cout << "Invalid index" << endl;
        return;
    }

    // 如果刪完會變空
    if (count == 1) {
        delete[] patients;
        patients = nullptr;
        count = 0;
        return;
    }

    // 開新的較小陣列
    Patient* newPatients = new Patient[count - 1];

    unsigned int j = 0;

    // 複製，跳過 index
    for (unsigned int i = 0; i < count; i++) {

        if (i == index)
            continue;

        newPatients[j] = patients[i];
        j++;
    }

    // 刪舊陣列
    delete[] patients;

    // 更新指標
    patients = newPatients;

    // 減少數量
    count--;
}

// 4) 顯示所有病患
void displayPatients(const Patient* patients, int count)
{
    if (count == 0 || patients == nullptr) {
        cout << "There is no patients in this hospital" << endl;
        return;
    }

    for (int i = 0; i < count; i++) {

        cout << patients[i].name
             << " (Age: " << patients[i].age
             << ", Condition: " << patients[i].condition
             << ")" << endl;
    }
}


// 測試用 main（方便你練習）
int main()
{
    Patient* patients = nullptr;
    unsigned int count = 0;

    addPatient(patients, count, "John Doe", 45, "Flu");
    addPatient(patients, count, "Jane Smith", 32, "Fractured Arm");
    addPatient(patients, count, "Alice Johnson", 27, "Allergy");

    cout << "Patients:" << endl;
    displayPatients(patients, count);

    cout << endl << "Remove index 1:" << endl;
    removePatient(patients, count, 1);

    displayPatients(patients, count);

    // 釋放記憶體
    delete[] patients;

    return 0;
}