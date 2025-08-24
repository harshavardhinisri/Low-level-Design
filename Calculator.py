from abc import ABC, abstractmethod

# Strategy Interface
class Operation(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

# Concrete Strategies
class Add(Operation):
    def execute(self, a, b):
        return a + b

class Subtract(Operation):
    def execute(self, a, b):
        return a - b

class Multiply(Operation):
    def execute(self, a, b):
        return a * b

class Divide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
class Mod(Operation):
    def execute(self, a, b):
        return a % b

# Context
class Calculator:
    def __init__(self, strategy: Operation):
        self.strategy = strategy

    def set_strategy(self, strategy: Operation):
        self.strategy = strategy  # dynamically change operation

    def calculate(self, a, b):
        return self.strategy.execute(a, b)

# Client code
if __name__ == "__main__":
    calc = Calculator(Add()) # Add() creates an object of Add strategy
    #So self.strategy in line 34 now holds the Add object.

    
    print("2 + 3 =", calc.calculate(2, 3))

    calc.set_strategy(Multiply())
    print("4 * 5 =", calc.calculate(4, 5))

    calc.set_strategy(Divide())
    print("10 / 2 =", calc.calculate(10, 2))

    calc.set_strategy(Mod())
    print("10 % 2 =", calc.calculate(10, 2))
