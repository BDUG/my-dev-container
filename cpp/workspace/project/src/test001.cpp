#include <iostream>

static int size = 0;

double mean (int a[]){
    int m;
    int sum = 0;
    for ( int i = 0; i<size; i++) {
        sum += a[i];
    }
    m = sum/ size;
    return m;
}

int main( int argc, char *argv[]){
    int a[10] = {1,2,3,4,5,6,7,8,9,10};
    size = 10;
    int *pa = a;
    double m = mean(pa);
    std::cout << m;
    return 0;
}