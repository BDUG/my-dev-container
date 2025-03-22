#ifndef GREETER_H
#define GREETER_H

#include <string>

class Greeter {
public:
    Greeter(const std::string& name);
    void say_hello() const;

private:
    std::string name_;
};

#endif
