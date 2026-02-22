#include <iostream>
#include <string>
using namespace std;

// 1. 定義 Book 結構
struct Book
{
    string title;
    bool available;
};



// 2. Pass-by-Value 函數（借書：暫時改變）
void borrowBookByValue(Book book)
{
    book.available = false;

    cout << "Inside borrowBookByValue() - Book status temporarily changed to: ";
    
    if(book.available)
        cout << "Yes" << endl;
    else
        cout << "No" << endl;
}



// 3. Pass-by-Reference 函數（還書：永久改變）
void returnBookByReference(Book &book)
{
    book.available = true;

    cout << "Inside returnBookByReference() - Book status Permanently changed to: ";
    
    if(book.available)
        cout << "Yes" << endl;
    else
        cout << "No" << endl;
}



// 4. Library Book Management System
void LBMS()
{
    cout << "Library Book Management System" << endl;
    cout << endl;

    // 建立 Book
    Book myBook;
    myBook.title = "C++ Programming";
    myBook.available = true;


    // 原始狀態
    cout << "Original book status:" << endl;
    cout << "Title: " << myBook.title 
         << ", Available: " << myBook.available << endl;
    cout << endl;


    // Pass-by-Value 借書
    cout << "Attempting to borrow the book by value:" << endl;
    
    borrowBookByValue(myBook);

    cout << endl;

    cout << "Book borrowed temporarily, status updated to: No" << endl;

    cout << "Original book status after borrowing by value:" << endl;
    cout << "Title: " << myBook.title 
         << ", Available: " << myBook.available << endl;

    cout << endl;


    // Pass-by-Reference 還書
    cout << "Returning the book by reference:" << endl;

    returnBookByReference(myBook);

    cout << endl;

    cout << "Book returned, status updated to: Yes" << endl;
    cout << endl;


    // 最終狀態
    cout << "Final book status:" << endl;
    cout << "Title: " << myBook.title 
         << ", Available: " << myBook.available << endl;
}



// main
int main()
{
    LBMS();
    return 0;
}