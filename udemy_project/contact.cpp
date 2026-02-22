#include <iostream>
#include <cstring>   // for strcpy, strcat
#include <string>

using namespace std;

/* ===========================
   1️⃣ Format Contact (C-style)
   =========================== */
void formatContactCStyle(char* destination,
                         const char* firstName,
                         const char* lastName,
                         const char* phoneNumber)
{
    // destination 必須夠大 (呼叫時保證)

    strcpy(destination, "Name: ");
    strcat(destination, firstName);
    strcat(destination, " ");
    strcat(destination, lastName);
    strcat(destination, ", Phone: ");
    strcat(destination, phoneNumber);
}


/* ===========================
   2️⃣ Format Contact (Modern string)
   =========================== */
string formatContactModern(const string& firstName,
                           const string& lastName,
                           const string& phoneNumber)
{
    return "Name: " + firstName + " " + lastName +
           ", Phone: " + phoneNumber;
}


/* ===========================
   3️⃣ Count Characters (C-style)
   =========================== */
int countTotalCharactersCStyle(const char* str)
{
    int count = 0;

    while (str[count] != '\0')   // 自己寫，不用 strlen
    {
        count++;
    }

    return count;
}


/* ===========================
   4️⃣ Count Characters (Modern string)
   =========================== */
int countTotalCharactersModern(const string& str)
{
    return str.length();   // 或 str.size();
}


/* ===========================
   🔹 測試 main (如果需要)
   =========================== */
int main()
{
    const char* firstName = "Alice";
    const char* lastName = "Walker";
    const char* phoneNumber = "+1-202-555-0147";

    // C-style
    char buffer[100];  // 必須夠大！
    formatContactCStyle(buffer, firstName, lastName, phoneNumber);
    cout << buffer << endl;

    // Modern string
    string result = formatContactModern("Alice", "Walker", "+1-202-555-0147");
    cout << result << endl;

    // Count test
    cout << countTotalCharactersCStyle("Alice") << endl;   // 5
    cout << countTotalCharactersModern("Walker") << endl;  // 6

    return 0;
}