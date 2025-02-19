from codecs import raw_unicode_escape_decode


class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit


class Building(SmartHouse):
    def __init__(self, name = None):
        self.name = name
        self.floors = []
    
    def addFloor(self, floor):
        self.floors.append(floor)

class Floor:
    def __init__(self, level):
        self.level = level
        self.rooms = []
        
    def getArea(self):
        total_area = sum(room.area for room in self.rooms)
        return total_area
    
    def addRoom(self, room):
        self.rooms.append(room)

class Room:
    def __init__(self, area, floor, name = None):
        self.name = name
        self.area = area
        self.floor = floor
        self.devices = []
        
    def addDevice(self, device):
        self.devices.append(device)
        
class Device:
    def __init__(self, id, producer, model, nickname, deviceType):
        self.id = id
        self.producer = producer
        self.model = model
        self.nickname = nickname
        self.deviceType = deviceType

class Sensor(Device):
    def __init__(self, id, producer, model, nickname, deviceType = 'sensor'):
        super().__init__(id, producer, model, nickname, deviceType)
        self.measureHistory = []
        
    def lastMeasure(self):
        if self.measureHistory:
            return self.measureHistory[-1]
        return None
    
    def addMeasure(self, Measurement):
        self.measureHistory.append(Measurement)

class Aktuator(Device):
    def __init__(self, id, producer, model, nickname, deviceType = 'aktuator'):
        super().__init__(id, producer, model, nickname, deviceType)
        self.state = 0
        
    def changeState(self, newState):
        self.state = newState
        
    def getState(self):
        return self.state
        
class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        
        floor = Floor(level)
        return floor
        

    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        room = Room(room_size, floor, room_name)
        floor.addRoom(room)
        pass


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
        
        allRooms = []
        
        for floor in self.floors:
            for room in floor.rooms:
                allRooms.append(room)
        
        return allRooms


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        totalArea = 0
        for floor in self.floors:
            totalArea += floor.getArea()
         
        return totalArea

    def register_device(self, room, device):
        """
        This methods registers a given device in a given room.
        """
        room.addDevice(device)
        pass

    
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

