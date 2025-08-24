from abc import ABC, abstractmethod
import threading

# ----------- Component -----------
class Pizza(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass

# ----------- Concrete Pizzas -----------
class Margherita(Pizza):
    def get_description(self) -> str:
        return "Margherita Pizza"

    def get_cost(self) -> float:
        return 5.0

class PepperoniPizza(Pizza):
    def get_description(self) -> str:
        return "Pepperoni Pizza"

    def get_cost(self) -> float:
        return 6.0

class VeggiePizza(Pizza):
    def get_description(self) -> str:
        return "Veggie Pizza"

    def get_cost(self) -> float:
        return 5.5

# ----------- Decorator -----------
class ToppingDecorator(Pizza, ABC):
    def __init__(self, pizza: Pizza):
        self.pizza = pizza

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass

# ----------- Concrete Toppings -----------
class Cheese(ToppingDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", Cheese"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.5

class PepperoniTopping(ToppingDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", Pepperoni"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + 2.0

class Veggies(ToppingDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", Veggies"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.0

# ----------- Factory -----------
class PizzaFactory:
    pizza_map = {
        "margherita": Margherita,
        "pepperoni": PepperoniPizza,
        "veggie": VeggiePizza
    }

    topping_map = {
        "cheese": Cheese,
        "pepperoni": PepperoniTopping,
        "veggies": Veggies
    }

    @staticmethod
    def create_pizza(base_type: str, toppings: list[str]) -> Pizza:
        base_cls = PizzaFactory.pizza_map.get(base_type.lower())
        if not base_cls:
            raise ValueError(f"Unknown pizza type: {base_type}")
        pizza = base_cls()

        for topping in toppings:
            topping_cls = PizzaFactory.topping_map.get(topping.lower())
            if not topping_cls:
                raise ValueError(f"Unknown topping: {topping}")
            pizza = topping_cls(pizza)

        return pizza

# ----------- Singleton Pizza Order Manager -----------
class PizzaOrderManager:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if PizzaOrderManager.__instance is not None:
            raise Exception("Use get_instance() instead of creating PizzaOrderManager directly")
        self.__orders = []

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(PizzaOrderManager, cls).__new__(cls)
                    cls.__instance.__orders = []
        return cls.__instance

    def place_order(self, pizza: Pizza):
        self.__orders.append(pizza)

    def cancel_order(self, index: int):
        if 0 <= index < len(self.__orders):
            return self.__orders.pop(index)
        raise IndexError("Invalid order index")

    def print_orders(self):
        print("Current Orders:")
        for i, pizza in enumerate(self.__orders, 1):
            print(f"{i}. {pizza.get_description()} - ${pizza.get_cost():.2f}")

# ----------- Client Code (No direct object creation) -----------
if __name__ == "__main__":
    manager = PizzaOrderManager.get_instance()

    orders_to_place = [
        ("margherita", ["cheese", "pepperoni", "veggies"]),
        ("pepperoni", ["cheese"]),
        ("veggie", ["veggies", "cheese"])
    ]

    for base, toppings in orders_to_place:
        pizza = PizzaFactory.create_pizza(base, toppings)
        manager.place_order(pizza)

    manager.print_orders()
