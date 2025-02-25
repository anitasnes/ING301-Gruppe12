from codecs import raw_unicode_escape_decode
from datetime import time
import random


class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit



class Floor:
    def __init__(self, level):
        self.level = level
        self.rooms = []
        
    def get_area(self):
        total_area = sum(room.area for room in self.rooms)
        return total_area
    
    def add_room(self, room):
        self.rooms.append(room)

class Room:
    def __init__(self, area, floor, name = None):
        self.name = name
        self.area = area
        self.floor = floor
        self.devices = []
        
    def add_device(self, device):
        self.devices.append(device)
        
class Device:
    def __init__(self, id, supplier, model_name, nickname, device_type):
        self.id = id
        self.supplier = supplier
        self.model_name = model_name
        self.nickname = nickname
        self.device_type = device_type
    
    def is_actuator(self):
        if self.device_Type == 'aktuator':
            return True
        return False
    
    def is_sensor(self):
        if self.device_type == 'sensor':
            return True
        return False
    
    def get_device_type(self):
        return self.nickname

class Sensor(Device):
    def __init__(self, id, producer, model, nickname, unit, deviceType = 'sensor'):
        super().__init__(id, producer, model, nickname, deviceType)
        self.unit = unit
        self.measure_history = []
        
    def last_measure(self):
        if self.measure_history:
            return self.measure_history[-1]
        return None
    
    def add_measure(self):
        timestamp = time.time()
        value = random.randint(0,100)
        measure = Measurement(timestamp, value, self.unit)
        self.add_measure_known(measure)

    def add_measure_known(self, Measurement):
        self.measure_history.append(Measurement)

class Aktuator(Device):
    def __init__(self, id, producer, model, nickname, deviceType = 'aktuator'):
        super().__init__(id, producer, model, nickname, deviceType)
        self.state = 0
        
    def turn_on(self):
        self.state = True
    
    def turn_off(self):
        self.state = False
        
    def is_active(self):
        if self.state != 0:
            return True
        return False
        
class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """
    def __init__(self, name = None):
        self.name = name
        self.floors = []

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        
        floor = Floor(level)
        self.floors.append(floor)
        return floor
        

    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        room = Room(room_size, floor, room_name)
        floor.add_room(room)
        return room


    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """

        return sorted(self.floors, key=lambda floor: floor.level)


    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        
        all_rooms = []
        
        for floor in self.floors:
            for room in floor.rooms:
                all_rooms.append(room)
        
        return all_rooms


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        total_area = 0
        for floor in self.floors:
            total_area += floor.get_area()
         
        return total_area

    def register_device(self, room, device):
        """
        This methods registers a given device in a given room.
        """
        room.add_device(device)
        return device

    
    def get_device(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        for floor in self.floors:
            for room in floor.rooms:
                for device in room.devices:
                    if device.id == device_id:
                        return device
        return None

