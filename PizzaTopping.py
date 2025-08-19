from abc import ABC, abstractmethod

# Component
class Pizza(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass

# Concrete Component
class Margherita(Pizza):
    def get_description(self) -> str:
        return "Margherita Pizza"

    def get_cost(self) -> float:
        return 5.0

# Decorator
class ToppingDecorator(Pizza, ABC):
    def __init__(self, pizza: Pizza):
        self.pizza = pizza

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass

# Concrete Decorators
class Cheese(ToppingDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", Cheese"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.5

class Pepperoni(ToppingDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", Pepperoni"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + 2.0

class Veggies(ToppingDecorator):
    def get_description(self) -> str:
        return self.pizza.get_description() + ", Veggies"

    def get_cost(self) -> float:
        return self.pizza.get_cost() + 1.0

# Client code
if __name__ == "__main__":
    pizza = Margherita()
    print(pizza.get_description(), "Cost:", pizza.get_cost())

    pizza = Cheese(pizza)
    pizza = Pepperoni(pizza)
    pizza = Veggies(pizza)
    print(pizza.get_description(), "Cost:", pizza.get_cost())
