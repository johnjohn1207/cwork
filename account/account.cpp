# include <iostream>
using namespace std;

double balance=0.0;
double* ptrBalance= &balance;

void viewBalance(double* account){
    cout<<"Current balance: $"<<*account<<endl;
}
void deposit(double* account){
    double deposit;
    cout<<"Enter deposit amount: ";
    cin>>deposit;
    if(deposit>0){
        * account=* account+deposit;
        cout<<"New balance: $"<<*account<<endl;
    }
    else{
        cout<<"Enter a valid command!"<<endl;
    }
}
void withdraw(double* account){
    double withdraw;
    cout<<"Enter withdraw amount: ";
    cin>>withdraw;
    if(withdraw> *account){
        cout<<"Insufficient funds!"<<endl;
    }
    else{
        *account-=withdraw;
        cout<<"New balance: $"<<*account<<endl;
    }
}

void accountGestion(double* account){
    char command;
    while(true){
        cout<<"Enter 'v' to view balance, 'd' to deposit, 'w' to withdraw, 'q' to quit:";
        cin>>command;
        switch(command){
            case 'v':
                viewBalance(account);
                break;
            case 'd':
                deposit(account);
                break;
            case 'w':
                withdraw(account);
                break;
            case 'q':
                cout<<"Good bye!"<<endl;
                return ;
            default:
                cout<<"Enter a valid command!"<<endl;
        }
    
    }
}

int main(){
    cout<<"Welcome to the account balance management system!"<<endl;
    accountGestion(ptrBalance);
    return 0;
}