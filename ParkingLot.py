from abc import ABC, abstractmethod
import threading

# ----------- Vehicle Types -----------
class VehicleType:
    CAR = "Car"
    BIKE = "Bike"

# ----------- Vehicle -----------
class Vehicle:
    def __init__(self, vehicle_type, plate_number):
        self.vehicle_type = vehicle_type
        self.plate_number = plate_number

# ----------- Vehicle Factory -----------
class VehicleFactory:
    vehicle_map = {
        "car": VehicleType.CAR,
        "bike": VehicleType.BIKE
    }

    @staticmethod
    def create_vehicle(vehicle_type: str, plate_number: str) -> Vehicle:
        vt = VehicleFactory.vehicle_map.get(vehicle_type.lower())
        if not vt:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        return Vehicle(vt, plate_number)

# ----------- Parking Spot -----------
class ParkingSpot:
    def __init__(self, spot_id, vehicle_type):
        self.spot_id = spot_id
        self.vehicle_type = vehicle_type
        self.is_free = True
        self.vehicle = None

    def park(self, vehicle: Vehicle):
        if self.is_free and self.vehicle_type == vehicle.vehicle_type:
            self.vehicle = vehicle
            self.is_free = False
            return True
        return False

    def leave(self):
        self.vehicle = None
        self.is_free = True

# ----------- Strategy Pattern -----------
class ParkingStrategy(ABC):
    @abstractmethod
    def find_spot(self, spots, vehicle: Vehicle):
        pass

class NearestSpotStrategy(ParkingStrategy):
    def find_spot(self, spots, vehicle: Vehicle):
        for spot in spots:
            if spot.is_free and spot.vehicle_type == vehicle.vehicle_type:
                return spot
        return None

# ----------- Singleton Parking Lot -----------
class ParkingLot:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, num_car_spots: int = 0, num_bike_spots: int = 0, strategy: ParkingStrategy = None):
        if ParkingLot.__instance is not None:
            raise Exception("Use get_instance() instead of creating ParkingLot directly")
        self.__spots = []
        self.__spots += [ParkingSpot(f"C{i}", VehicleType.CAR) for i in range(num_car_spots)]
        self.__spots += [ParkingSpot(f"B{i}", VehicleType.BIKE) for i in range(num_bike_spots)]
        self.strategy = strategy or NearestSpotStrategy()

    @classmethod
    def get_instance(cls, num_car_spots: int = 0, num_bike_spots: int = 0, strategy: ParkingStrategy = None):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(ParkingLot, cls).__new__(cls)
                    cls.__instance.__spots = []
                    cls.__instance.__spots += [ParkingSpot(f"C{i}", VehicleType.CAR) for i in range(num_car_spots)]
                    cls.__instance.__spots += [ParkingSpot(f"B{i}", VehicleType.BIKE) for i in range(num_bike_spots)]
                    cls.__instance.strategy = strategy or NearestSpotStrategy()
        return cls.__instance

    def park_vehicle(self, vehicle: Vehicle):
        spot = self.strategy.find_spot(self.__spots, vehicle)
        if spot and spot.park(vehicle):
            print(f"{vehicle.vehicle_type} {vehicle.plate_number} parked at spot {spot.spot_id}")
            return True
        print(f"No available spot for {vehicle.vehicle_type} {vehicle.plate_number}")
        return False

    def leave_spot(self, spot_id: str):
        for spot in self.__spots:
            if spot.spot_id == spot_id:
                spot.leave()
                print(f"Spot {spot_id} is now free")
                return True
        print(f"Spot {spot_id} not found")
        return False

# ----------- Client Code (No direct object creation) -----------
if __name__ == "__main__":
    lot = ParkingLot.get_instance(num_car_spots=2, num_bike_spots=2)  # Singleton accessor

    # Create vehicles via factory
    vehicles_to_park = [
        ("car", "CAR123"),
        ("bike", "BIKE123"),
        ("car", "CAR999")
    ]
    vehicles = [VehicleFactory.create_vehicle(v_type, plate) for v_type, plate in vehicles_to_park]

    # Park vehicles
    for v in vehicles:
        lot.park_vehicle(v)

    # Leave a spot
    lot.leave_spot("C0")

    # Check Singleton behavior
    lot2 = ParkingLot.get_instance()
    print("lot and lot2 are same:", lot is lot2)

