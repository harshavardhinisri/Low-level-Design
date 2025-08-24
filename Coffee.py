from abc import ABC, abstractmethod

# ----------- Base Coffee (Component) -----------
class Coffee(ABC):
    @abstractmethod
    def get_description(self):
        pass
    
    @abstractmethod
    def get_price(self):
        pass


# ----------- Concrete Coffees -----------
class Espresso(Coffee):
    def get_description(self):
        return "Espresso Coffee"
    
    def get_price(self):
        return 5.0

class Mocha(Coffee):
    def get_description(self):
        return "Mocha Coffee"
    
    def get_price(self):
        return 6.0

class Latte(Coffee):
    def get_description(self):
        return "Latte Coffee"
    
    def get_price(self):
        return 5.5

class Cappuccino(Coffee):
    def get_description(self):
        return "Cappuccino Coffee"
    
    def get_price(self):
        return 6.5


# ----------- Topping Decorator -----------
class Topping(Coffee, ABC):
    def __init__(self, coffee: Coffee):
        self.coffee = coffee


# ----------- Concrete Toppings -----------
class IceCream(Topping):
    def get_description(self):
        return self.coffee.get_description() + ", Ice Cream"
    
    def get_price(self):
        return self.coffee.get_price() + 1.0

class Sugar(Topping):
    def get_description(self):
        return self.coffee.get_description() + ", Sugar"
    
    def get_price(self):
        return self.coffee.get_price() + 0.5

class WhippedCream(Topping):
    def get_description(self):
        return self.coffee.get_description() + ", Whipped Cream"
    
    def get_price(self):
        return self.coffee.get_price() + 1.5

class Sweetener(Topping):
    def get_description(self):
        return self.coffee.get_description() + ", Sweetener"
    
    def get_price(self):
        return self.coffee.get_price() + 0.7


# ----------- Coffee Factory -----------
class CoffeeFactory:
    coffee_map = {
        "espresso": Espresso,
        "mocha": Mocha,
        "latte": Latte,
        "cappuccino": Cappuccino
    }

    topping_map = {
        "icecream": IceCream,
        "sugar": Sugar,
        "whippedcream": WhippedCream,
        "sweetener": Sweetener
    }

    @staticmethod
    def create_coffee(base_type: str, toppings: list[str]):
        # create base coffee
        base_cls = CoffeeFactory.coffee_map.get(base_type.lower())
        if not base_cls:
            raise ValueError(f"Unknown coffee type: {base_type}")
        coffee = base_cls()

        # add toppings
        for topping in toppings:
            topping_cls = CoffeeFactory.topping_map.get(topping.lower())
            if not topping_cls:
                raise ValueError(f"Unknown topping: {topping}")
            coffee = topping_cls(coffee)

        return coffee


# ----------- Singleton Order Manager -----------
import threading

class OrderManager:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        """Prevent direct instantiation from outside"""
        if OrderManager.__instance is not None:
            raise Exception("Use get_instance() instead of creating OrderManager directly")

    @classmethod
    def get_instance(cls):
        """Thread-safe accessor for singleton"""
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(OrderManager, cls).__new__(cls)
                    cls.__instance.__order = []
        return cls.__instance

    def place_order(self, coffee):
        self.__order.append(coffee)

    def cancel_order(self, index):
        if 0 <= index < len(self.__order):
            return self.__order.pop(index)
        else:
            raise IndexError("Invalid order index")

    def print_order(self):
        print("Your Order:")
        for i, coffee in enumerate(self.__order, 1):
            print(f"{i}. {coffee.get_description()} - ${coffee.get_price():.2f}")

if __name__ == "__main__":
    # Get the singleton via accessor
    manager = OrderManager.get_instance()

    coffee1 = CoffeeFactory.create_coffee("espresso", ["icecream", "sugar"])
    coffee2 = CoffeeFactory.create_coffee("mocha", ["whippedcream"])
    coffee3 = CoffeeFactory.create_coffee("latte", [])

    manager.place_order(coffee1)
    manager.place_order(coffee2)
    manager.place_order(coffee3)

    manager.print_order()
