#include <iostream>
#include <string>
#include <iomanip> // for setprecision
using namespace std;


// 1. 定義 Student struct
struct Student
{
    int id;
    string name;
    double grades[3];
    double average;
};



// Function 1: initializeStudents
void initializeStudents(Student students[], int count)
{
    for(int i = 0; i < count; i++)
    {
        cout << "Enter Student ID: ";
        cin >> students[i].id;

        cin.ignore(); // 清除 buffer

        cout << "Enter Student Name: ";
        getline(cin, students[i].name);

        cout << "Enter 3 grades: ";

        for(int j = 0; j < 3; j++)
        {
            cin >> students[i].grades[j];
        }

        cout << endl;
    }
}



// Function 2: calculateAverage (Pass-by-Reference)
void calculateAverage(Student &student)
{
    double sum = 0;

    for(int i = 0; i < 3; i++)
    {
        sum += student.grades[i];
    }

    student.average = sum / 3;

    cout << "Processing student grades..." << endl;
    cout << "Average student " 
         << student.name 
         << " grade is : "
         << fixed << setprecision(2)
         << student.average << endl;
}



// Function 3: displayStudents
void displayStudents(const Student students[], int count)
{
    cout << endl;
    cout << "Student Details:" << endl;

    for(int i = 0; i < count; i++)
    {
        cout << "ID: " << students[i].id
             << ", Name: " << students[i].name
             << ", Grades: ";

        for(int j = 0; j < 3; j++)
        {
            cout << students[i].grades[j] << " ";
        }

        cout << ", Average: "
             << fixed << setprecision(2)
             << students[i].average << endl;
    }
}



// Main
int main()
{
    const int COUNT = 2;

    Student students[COUNT];

    // 初始化學生
    initializeStudents(students, COUNT);


    // 計算每個學生平均
    for(int i = 0; i < COUNT; i++)
    {
        calculateAverage(students[i]);
    }


    // 顯示學生資料
    displayStudents(students, COUNT);

    return 0;
}