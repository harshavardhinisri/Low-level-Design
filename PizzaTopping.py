from abc import ABC, abstractmethod

# Base Pizza class
class Pizza:
    def __init__(self, size):
        self.size = size
        self.toppings = []

    def add_topping(self, topping):
        self.toppings.append(topping)

    def __str__(self):
        return f"Pizza(size={self.size}, toppings={self.toppings})"

# Abstract Builder
class PizzaBuilder(ABC):
    @abstractmethod
    def add_cheese(self):
        pass

    @abstractmethod
    def add_pepperoni(self):
        pass

    @abstractmethod
    def add_veggies(self):
        pass

    @abstractmethod
    def build(self):
        pass

# Concrete Builder
class CustomPizzaBuilder(PizzaBuilder):
    def __init__(self, size):
        self.pizza = Pizza(size)

    def add_cheese(self):
        self.pizza.add_topping("Cheese")
        return self  # allows chaining

    def add_pepperoni(self):
        self.pizza.add_topping("Pepperoni")
        return self

    def add_veggies(self):
        self.pizza.add_topping("Veggies")
        return self

    def build(self):
        return self.pizza

# Director (optional, helps build standard pizzas)
class PizzaDirector:
    def __init__(self, builder):
        self.builder = builder

    def make_margherita(self):
        return self.builder.add_cheese().build()

    def make_pepperoni_pizza(self):
        return self.builder.add_cheese().add_pepperoni().build()

    def make_veggie_pizza(self):
        return self.builder.add_cheese().add_veggies().build()


# ====== Usage ======
if __name__ == "__main__":
    builder = CustomPizzaBuilder("Medium")
    margherita = PizzaDirector(builder).make_margherita()
    print(margherita)

    custom_pizza = CustomPizzaBuilder("Large").add_cheese().add_pepperoni().add_veggies().build()
    print(custom_pizza)
