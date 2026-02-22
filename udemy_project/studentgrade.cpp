#include <iostream>
using namespace std;
 
void studentGrade()
{
    unsigned int N;
    double lowestGrade = 100.0;
    double highestGrade = 0.0;
    double averageGrade = 0.0;
    cout << "Enter the number of students: ";
    cin >> N;
    double* grades = new double[N];
    
    for (unsigned int i = 0; i < N; i++)
    {
        cout << "Enter grade for student " << i+1 << ": ";
        cin >> grades[i];
        cout << grades[i] << endl;
        if (grades[i] > highestGrade)
        {
            highestGrade = grades[i];
        }
        
        if (grades[i] < lowestGrade)
        {
            lowestGrade = grades[i];
        }
        averageGrade += grades[i];
    }
    averageGrade /= N;
    
    cout << "Average grade: " << averageGrade << endl;  
    cout << "Highest grade: " << highestGrade << endl;
    cout << "Lowest grade: " << lowestGrade << endl;
    
    delete[] grades;
}

int main()
{
    studentGrade();
    return 0;
}