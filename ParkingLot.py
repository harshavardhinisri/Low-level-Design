from abc import ABC, abstractmethod

# Vehicle Types
class VehicleType:
    CAR = "Car"
    BIKE = "Bike"

# Vehicle
class Vehicle:
    def __init__(self, vehicle_type, plate_number):
        self.vehicle_type = vehicle_type
        self.plate_number = plate_number

# Parking Spot
class ParkingSpot:
    def __init__(self, spot_id, vehicle_type):
        self.spot_id = spot_id
        self.vehicle_type = vehicle_type
        self.is_free = True
        self.vehicle = None

    def park(self, vehicle):
        if self.is_free and self.vehicle_type == vehicle.vehicle_type:
            self.vehicle = vehicle
            self.is_free = False
            return True
        return False

    def leave(self):
        self.vehicle = None
        self.is_free = True

# Strategy Pattern - Parking Strategy
class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, spots, vehicle):
        pass

class NearestSpotStrategy(ParkingStrategy):
    def find_spot(self, spots, vehicle):
        for spot in spots:
            if spot.is_free and spot.vehicle_type == vehicle.vehicle_type:
                return spot
        return None

# Singleton ParkingLot
class ParkingLot:
    __instance = None

    def __new__(cls, num_car_spots, num_bike_spots, strategy=None):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls) #calls the parent (object) class’s __new__ method, 
            #which actually allocates memory for the new instance of cls
            cls.__instance.spots = []
            cls.__instance.spots += [ParkingSpot(f"C{i}", VehicleType.CAR) for i in range(num_car_spots)]
            cls.__instance.spots += [ParkingSpot(f"B{i}", VehicleType.BIKE) for i in range(num_bike_spots)]
            cls.__instance.strategy = strategy or NearestSpotStrategy()
        return cls.__instance

    def park_vehicle(self, vehicle):
        spot = self.strategy.find_spot(self.spots, vehicle)
        if spot and spot.park(vehicle):
            print(f"{vehicle.vehicle_type} {vehicle.plate_number} parked at spot {spot.spot_id}")
            return True
        print(f"No available spot for {vehicle.vehicle_type} {vehicle.plate_number}")
        return False

    def leave_spot(self, spot_id):
        for spot in self.spots:
            if spot.spot_id == spot_id:
                spot.leave()
                print(f"Spot {spot_id} is now free")
                return True
        print(f"Spot {spot_id} not found")
        return False

# --- Client code ---
if __name__ == "__main__":
    lot = ParkingLot(2, 2)  # Singleton instance
    lot2 = ParkingLot(5, 5) # Will still return same instance as `lot`

    car1 = Vehicle(VehicleType.CAR, "CAR123")
    bike1 = Vehicle(VehicleType.BIKE, "BIKE123")
    car2 = Vehicle(VehicleType.CAR, "CAR999")

    lot.park_vehicle(car1)
    lot.park_vehicle(bike1)
    lot.park_vehicle(car2)

    lot.leave_spot("C0")

    # Check Singleton behavior
    print("lot and lot2 are same:", lot is lot2)
