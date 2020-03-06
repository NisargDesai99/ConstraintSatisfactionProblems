#include <iostream>
#include <fstream>
#include <string>
#include <cmath>

#define SIZE 40

using namespace std;

enum SERVICE_TYPE {POLICE_DEPARTMENT, HOSPITAL, FIRE_STATION};

struct Service {
    int serviceID;
    double xc;
    double yc;
    SERVICE_TYPE sType;
    string cityName;
    int calls;
};

SERVICE_TYPE findNearestService(double, double, Service*, int);
void findNearestPolice();
void findNearestHospital();
void findNearestFire();

int main() {
    
    char selection;
    bool isLocEntered = false;
    bool isExit = false;
    double xval = 0.0;
    double yval = 0.0;
    int tempSType;
    
    Service *sInfoArray;
    sInfoArray = new Service[SIZE];
    
    fstream infoFile;
    infoFile.open("serviceInfo.txt", ios::in);
    
    if (infoFile.fail()) {
        cout << "The file failed to open. " << endl;
    } else {
        cout << "The file opened successfully. " << endl;
    }
    
    int counter = 0;
    while (!infoFile.eof()) {
        infoFile >> (sInfoArray + counter)->serviceID;              //Take Service ID
        
        infoFile >> (sInfoArray + counter)->xc;                     //Take x position
        infoFile >> (sInfoArray + counter)->yc;                     //Take y position
        
        infoFile >> tempSType;                                      //Take enum as int
        (sInfoArray + counter)->sType = SERVICE_TYPE(tempSType);    //Cast int as enum
        
        counter++;                                                  //Increment counter
    }
    
    while (!isExit) {
        cout << "Choose one of the following. Enter a-b. \n"
        << "a) Enter your location (x,y) \n"
        << "b) Find the nearest service \n"
        << "c) Find the nearest POLICE DEPARTMENT \n"
        << "d) Find the nearest HOSPITAL \n"
        << "e) Find the nearest FIRE STATION \n"
        << "f) Exit " << endl;
        cin >> selection;
        cout << endl;
        
        if (selection == 'a') {
            cout << "Enter the x coordinate: "; cin >> xval;
            cout << "Enter the y coordinate: "; cin >> yval;
            isLocEntered = true;
        }
        else if (isLocEntered && (selection == 'b')) {
            SERVICE_TYPE s;
            s = findNearestService(xval, yval, sInfoArray, counter);
            cout << "The nearest service to you is a " << s << ". " << endl << endl;
        } else if (isLocEntered && (selection == 'c')) {
            //findNearestPoliceDept();
        } else if (isLocEntered && (selection == 'd')) {
            //findNearestHospital();
        } else if (isLocEntered && (selection == 'e')) {
            //findNearestFStation();
        } else if (isLocEntered && (selection == 'f')) {
            cout << "You chose to exit the program. " << endl;
            isExit = true;
        } else {
            cout << "Invalid choice. Try again." << endl;
        }
        if (isExit) {
            exit(1);
        }
    }

    
    return 0;
}

SERVICE_TYPE findNearestService(double x, double y, Service *infoArr, int arrSize) {
    infoArr = new Service[arrSize];
    
    
    return HOSPITAL;
}

void findNearestPolice() {
    
}





