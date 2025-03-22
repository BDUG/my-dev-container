#include "../include/greeter.h"
#include <iostream>

Greeter::Greeter(const std::string& name) : name_(name) {}

void Greeter::say_hello() const {
    std::cout << "Hello, " << name_ << "!" << std::endl;
}
