from enum import Enum
from collections import deque
from abc import ABC, abstractmethod
import threading

# --- Enums ---
class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class ElevatorState(Enum):
    IDLE = "Idle"
    MOVING = "Moving"
    STOPPED = "Stopped"

# --- Elevator ---
class Elevator:
    def __init__(self, id, max_floor):
        self.id = id
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.state = ElevatorState.IDLE
        self.requests = deque()
        self.max_floor = max_floor

    def add_request(self, floor):
        if 0 <= floor <= self.max_floor:
            self.requests.append(floor)

    def move(self):
        if not self.requests:
            self.direction = Direction.IDLE
            self.state = ElevatorState.IDLE
            return
        
        next_floor = self.requests.popleft()
        if next_floor > self.current_floor:
            self.direction = Direction.UP
        elif next_floor < self.current_floor:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE

        self.state = ElevatorState.MOVING
        print(f"Elevator {self.id} moving {self.direction.name} to {next_floor}")

        self.current_floor = next_floor
        self.state = ElevatorState.STOPPED
        print(f"Elevator {self.id} stopped at {self.current_floor}")

        if not self.requests:
            self.state = ElevatorState.IDLE
            self.direction = Direction.IDLE

# --- Strategy Pattern ---
class ElevatorStrategy(ABC):
    @abstractmethod
    def select_elevator(self, elevators, requested_floor):
        pass

class RoundRobinStrategy(ElevatorStrategy):
    def __init__(self):
        self.index = 0

    def select_elevator(self, elevators, requested_floor):
        print(f"Strategy for floor {requested_floor}")
        elevator = elevators[self.index]
        self.index = (self.index + 1) % len(elevators)
        return elevator

# --- Singleton Elevator Controller ---
class ElevatorController:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, num_elevators: int, max_floor: int, strategy: ElevatorStrategy = None):
        if ElevatorController.__instance is not None:
            raise Exception("Use get_instance() instead of creating ElevatorController directly")
        self.__elevators = [Elevator(i, max_floor) for i in range(num_elevators)]
        self.strategy = strategy or RoundRobinStrategy()

    @classmethod
    def get_instance(cls, num_elevators: int = 2, max_floor: int = 10, strategy: ElevatorStrategy = None):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(ElevatorController, cls).__new__(cls)
                    cls.__instance.__elevators = [Elevator(i, max_floor) for i in range(num_elevators)]
                    cls.__instance.strategy = strategy or RoundRobinStrategy()
        return cls.__instance

    def request_elevator(self, floor):
        elevator = self.strategy.select_elevator(self.__elevators, floor)
        elevator.add_request(floor)
        print(f"Request for floor {floor} assigned to Elevator {elevator.id}")

    def step(self):
        for elevator in self.__elevators:
            elevator.move()

# --- Client code (No direct object creation) ---
if __name__ == "__main__":
    controller = ElevatorController.get_instance(num_elevators=2, max_floor=10)

    floors_to_request = [5, 2, 8]
    for floor in floors_to_request:
        controller.request_elevator(floor)

    for _ in range(3):
        controller.step()
