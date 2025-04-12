#include <iostream>
#include <memory>
#include <vector>

// Observer Interface
class IObserver {
public:
    virtual ~IObserver() = default;
    virtual void update(int newValue) = 0;
};

// Concrete Observer
class Observer : public IObserver {
    int id_;
public:
    Observer(int id) : id_(id) {}

    void update(int newValue) override {
        std::cout << "Observer :" << id_ << " received update: " << newValue << "\n";
    }
};

// Subject Class
class Subject {
    int value_;
    std::vector<std::weak_ptr<IObserver>> observers_;

public:
    void attach(const std::shared_ptr<IObserver>& observer) {
        observers_.push_back(observer);
    }

    void setValue(int value) {
        value_ = value;
        notify();
    }

    void notify() {
        /*observers_.erase(
            std::remove_if(
                observers_.begin(), observers_.end(),
                [](const std::weak_ptr<IObserver>& weakObserver) {
                    return weakObserver.expired();
                }),
            observers_.end()
        );*/

        for (const auto& weakObserver : observers_) {
            if (auto observer = weakObserver.lock()) {
                observer->update(value_);
            }
        }
    }
};

int main() {
    Subject subject;

    auto observer1 = std::make_shared<Observer>(1);
    {
        auto observer2 = std::make_shared<Observer>(2);

        subject.attach(observer1);
        subject.attach(observer2);

        subject.setValue(10); // Notify all observers
    } // observer1 and observer2 are out of scope here, observers will be automatically removed

    subject.setValue(20); // No observers left, no notification happens

    return 0;
}
