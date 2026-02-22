#include <iostream>
using namespace std;

// 1) Allocate memory
void allocateMemory(int*& arr, int& size) {
    cout << "Enter number of elements: ";
    int n;
    cin >> n;

    if (n <= 0) {
        cout << "Invalid size. Allocation aborted.\n";
        return;
    }
    if (arr != nullptr) {
        cout << "Memory already allocated. Please deallocate first.\n";
        return;
    }

    arr = new int[n];
    size = n;
    cout << "Memory allocated for " << size << " integers.\n";
}

// 2) Fill memory
void fillMemory(int* arr, int size) {
    if (arr == nullptr || size <= 0) {
        cout << "Memory not allocated yet.\n";
        return;
    }

    cout << "Enter " << size << " integer(s):\n";
    for (int i = 0; i < size; i++) {
        cout << "[" << i << "]: ";
        cin >> arr[i];
    }
    // (no output after filling)
}

// 3) Display memory
void displayMemory(int* arr, int size) {
    if (arr == nullptr || size <= 0) {
        cout << "Memory not allocated yet.\n";
        return;
    }

    cout << "Array contents:\n";
    for (int i = 0; i < size; i++) {
        cout << "[" << i << "] = " << arr[i] << "\n";
    }
}

// 4) Deallocate memory
void deallocateMemory(int*& arr, int& size) {
    if (arr == nullptr) {
        cout << "No memory to deallocate.\n";
        return;
    }

    delete[] arr;
    arr = nullptr;
    size = 0;
    cout << "Memory deallocated.\n";
}

int mainFunc() {
    int* arr = nullptr;
    int size = 0;

    while (true) {
        cout << "=== Memory Management Simulator ===\n";
        cout << "1. Allocate memory\n";
        cout << "2. Fill memory\n";
        cout << "3. Display memory\n";
        cout << "4. Deallocate memory\n";
        cout << "5. Exit\n";
        cout << "Choice: ";

        int choice;
        cin >> choice;

        switch (choice) {
            case 1: allocateMemory(arr, size); break;
            case 2: fillMemory(arr, size); break;
            case 3: displayMemory(arr, size); break;
            case 4: deallocateMemory(arr, size); break;
            case 5:
                if (arr != nullptr) {
                    delete[] arr;
                    arr = nullptr;
                    size = 0;
                }
                cout << "Exiting program. Goodbye!\n";
                return 0;
            default:
                cout << "Invalid choice. Please try again.\n";
                break;
        }
    }
}

int main() {
    return mainFunc();
}