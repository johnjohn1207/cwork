#include <iostream>
using namespace std;
 
void add(double a, double b)
{
    cout << "Result: " << a << " + " << b << " = " << a + b << endl;
}
 
void subtract(double a, double b)
{
    cout << "Result: " << a << " - " << b << " = " << a - b << endl;
}
 
void multiply(double a, double b)
{
    cout << "Result: " << a << " * " << b << " = " << a * b << endl;
}
 
void divide(double a, double b)
{
    if (b  != 0)
    {
        cout << "Result: " << a << " / " << b << " = " << a / b << endl;
    }
    else
    {
        cout << "Error: Division by zero is not allowed." << endl;
    }
}
 
void menu()
{
    bool exitBool = false;
    unsigned int operation;
    double number1, number2;
 
    while(!exitBool)
    {
        cout << endl << "--- Basic Calculator ---" << endl;
        cout << "1. Add" << endl;
        cout << "2. Subtract" << endl;
        cout << "3. Multiply" << endl;
        cout << "4. Divide" << endl;
        cout << "5. Exit" << endl;
        cout << "Enter choice (1-5): " << endl;
        cin >> operation;
        
        switch(operation)
        {
            case 1 :
                cout << "Enter first number: ";
                cin >> number1;
                cout << "Enter second number: ";
                cin >> number2;
                add(number1, number2);
                break;
            case 2 :
                cout << "Enter first number: ";
                cin >> number1;
                cout << "Enter second number: ";
                cin >> number2;
                subtract(number1, number2);
                break;
            case 3 :
                cout << "Enter first number: ";
                cin >> number1;
                cout << "Enter second number: ";
                cin >> number2;
                multiply(number1, number2);
                break;
            case 4 :
                cout << "Enter first number: ";
                cin >> number1;
                cout << "Enter second number: ";
                cin >> number2;
                divide(number1, number2);
                break;
            case 5 :
                exitBool = true;
                cout << "Exiting program. Goodbye!";
                break;
            default :
                cout << "Invalid choice. Please enter a number between 1 and 5." << endl;
                break;
        }
    }
}
int main()
{
    menu();
    return 0;
}