from abc import ABC, abstractmethod

# ----------- Strategy Interface -----------
class Operation(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

# ----------- Concrete Strategies -----------
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

# ----------- Strategy Factory -----------
class OperationFactory:
    operation_map = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
        "mod": Mod
    }

    @staticmethod
    def create_operation(op_type: str) -> Operation:
        op_cls = OperationFactory.operation_map.get(op_type.lower())
        if not op_cls:
            raise ValueError(f"Unknown operation: {op_type}")
        return op_cls()  # Return instance of strategy


# ----------- Singleton Calculator -----------
import threading

class Calculator:
    __instance = None
    __lock = threading.Lock()

    def __init__(self):
        if Calculator.__instance is not None:
            raise Exception("Use get_instance() instead of creating Calculator directly")
        self.strategy = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(Calculator, cls).__new__(cls)
                    cls.__instance.strategy = None
        return cls.__instance

    def set_strategy(self, strategy: Operation):
        self.strategy = strategy

    def calculate(self, a, b):
        if not self.strategy:
            raise Exception("No strategy set")
        return self.strategy.execute(a, b)


# ----------- Client Code (No direct object creation) -----------
if __name__ == "__main__":
    calc = Calculator.get_instance()  # Singleton accessor

    # Use factory to create strategies
    calc.set_strategy(OperationFactory.create_operation("add"))
    print("2 + 3 =", calc.calculate(2, 3))

    calc.set_strategy(OperationFactory.create_operation("multiply"))
    print("4 * 5 =", calc.calculate(4, 5))

    calc.set_strategy(OperationFactory.create_operation("divide"))
    print("10 / 2 =", calc.calculate(10, 2))

    calc.set_strategy(OperationFactory.create_operation("mod"))
    print("10 % 2 =", calc.calculate(10, 2))
