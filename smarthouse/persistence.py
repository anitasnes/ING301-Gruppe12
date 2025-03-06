import sqlite3
from typing import Optional
from smarthouse.domain import Measurement, SmartHouse, Aktuator, Sensor, Floor

class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, file: str) -> None:
        self.file = file 
        self.conn = sqlite3.connect(file, check_same_thread=False)

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    
    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """
        HOUSE = SmartHouse()
        cursor = self.conn.cursor()
        cursor.execute("SELECT floor FROM rooms group by floor")

        for row in cursor.fetchall():
            floor_value = int(row[0])
            floor = Floor(floor_value)
            HOUSE.register_floor(floor)
     
        cursor.execute("SELECT floor, area, name FROM  rooms")
        floors_in_house = HOUSE.get_floors()
        for row in cursor.fetchall():
            for floor_c in floors_in_house:
                if floor_c.level == row[0]:
                    HOUSE.register_room(floor_c, row[1], row[2])

                

        cursor.execute("SELECT r.name, d.id, d.supplier, d.product, d.kind, d.category FROM devices AS d INNER JOIN rooms AS r ON d.room = r.id")
        rooms = HOUSE.get_rooms()
        for row in cursor.fetchall():
            for room in rooms:
                if(row[0] == room.room_name):
                    if(row[5] == "actuator"):
                        device = Aktuator(row[1], row[2], row[3], row[4])
                        HOUSE.register_device(room,device)
                    else:
                        device = Sensor(row[1], row[2], row[3], row[4])
                        HOUSE.register_device(room,device)

            
        cursor.execute("SELECT device, ts, value, unit FROM measurements")
        for row in cursor.fetchall():
            device = HOUSE.get_device_by_id(row[0])
            if device:
                measurement = Measurement(row[1], row[2], row[3])
                device.add_measurement_known(measurement)
            else:
                print(f"Enhet med ID {row[0]} finnes ikke i huset.")

            
        return HOUSE


    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        # TODO: After loading the smarthouse, continue here
        return NotImplemented


    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        # TODO: Implement this method. You will probably need to extend the existing database structure: e.g.
        #       by creating a new table (`CREATE`), adding some data to it (`INSERT`) first, and then issue
        #       and SQL `UPDATE` statement. Remember also that you will have to call `commit()` on the `Connection`
        #       stored in the `self.conn` instance variable.
        pass


    # statistics

    
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and 
        the values are floating point numbers containing the average temperature that day.
        """
        # TODO: This and the following statistic method are a bit more challenging. Try to design the respective 
        #       SQL statements first in a SQL editor like Dbeaver and then copy it over here.  
        return NotImplemented

    
    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        # TODO: implement
        return NotImplemented

