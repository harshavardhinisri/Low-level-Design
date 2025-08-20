from enum import Enum
from collections import deque
from abc import ABC, abstractmethod
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

    def move(self): #Prevents the elevator from trying to move when there are no requests.
        if not self.requests:
            self.direction  = Direction.IDLE
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

        if not self.requests:  #Just finished processing all requests, update elevator to idle.
            self.state = ElevatorState.IDLE
            self.direction = Direction.IDLE

# --- Strategy Pattern ---
class ElevatorStrategyPattern(ABC):
    @abstractmethod
    def select_elevator(self, elevators, requested_floor):
        pass

class Strategy(ElevatorStrategyPattern):
    def __init__(self):
        self.index = 0
    def select_elevator(self, elevators, requested_floor): #round robin
        print(f"Strategy for floor {requested_floor}")
        elevator = elevators[self.index]
        self.index = (self.index + 1) % len(elevators)
        return elevator
    
# --- Elevator Controller ---
class ElevatorController:
    __instance = None

    def __new__(cls, num_elevators, max_floor, strategy = None):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.elevators = [Elevator(i, max_floor) for i in range(num_elevators)]
            cls.__instance.strategy = strategy or Strategy()
        return cls.__instance
    
    def request_elevator(self, floor):
        elevator = self.strategy.select_elevator(self.elevators, floor)
        elevator.add_request(floor)
        print(f"Request for floor {floor} assigned to Elevator {elevator.id}")

    def step(self):
        for elevator in self.elevators:
            elevator.move()

if __name__ == "__main__":
    controller = ElevatorController(num_elevators=2, max_floor=10, strategy=Strategy())
    controller.request_elevator(5)
    controller.request_elevator(2)
    controller.request_elevator(8)

    for _ in range(3):
        controller.step()



