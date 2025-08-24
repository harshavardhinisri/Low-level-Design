from abc import ABC, abstractmethod

# Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, order):
        pass

# Concrete Observers
class Customer(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, order):
        print(f"Hello, {self.name}! Order #{order.get_id()} is now {order.get_status()}")

class Restaurant(Observer):
    def __init__(self, name):
        self.restaurant_name = name

    def update(self, order):
        print(f"Restaurant {self.restaurant_name}: Order #{order.get_id()} is now {order.get_status()}")

class DeliveryDriver(Observer):
    def __init__(self, name):
        self.driver_name = name

    def update(self, order):
        print(f"Driver {self.driver_name}: Order #{order.get_id()} is now {order.get_status()}")

class CallCenter(Observer):
    def update(self, order):
        print(f"Call center: Order #{order.get_id()} is now {order.get_status()}")

# Subject
class Order:
    def __init__(self, order_id):
        self._id = order_id
        self._status = "Order Placed"
        self._observers = []

    def get_id(self):
        return self._id

    def get_status(self):
        return self._status

    def set_status(self, new_status):
        self._status = new_status
        self._notify_observers()

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self):
        for observer in self._observers:
            observer.update(self)

# Example usage
if __name__ == "__main__":
    order1 = Order(123)

    customer1 = Customer("Customer 1")
    restaurant1 = Restaurant("Rest 1")
    driver1 = DeliveryDriver("Driver 1")
    call_center = CallCenter()

    # Attach observers
    order1.attach(customer1)
    order1.attach(restaurant1)
    order1.attach(driver1)
    order1.attach(call_center)

    # Simulate order status updates
    order1.set_status("Out for Delivery")

    # Detach an observer
    order1.detach(call_center)

    # Simulate more order status updates
    order1.set_status("Delivered")
