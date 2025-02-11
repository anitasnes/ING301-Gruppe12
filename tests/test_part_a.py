from unittest import TestCase, main
from smarthouse.domain import SmartHouse
from demo_house import DEMO_HOUSE as h

class TestPartA(TestCase):

    # Level 1 Basic: Does registration of floors, rooms, and devices work + simple queries about them

    def test_basic_no_of_rooms(self):
        self.assertEqual(len(h.get_rooms()), 12)

    def test_basic_get_area_size(self):
        self.assertEqual(h.get_area(), 156.55)

    def test_basic_get_no_of_devices(self):
        self.assertEqual(len(h.get_devices()), 14)

    def test_basic_get_device_by_id(self):
        # device id does not exist
        self.assertIsNone(h.get_device_by_id("9e5b8274-4e77-4e8e-80d2-b40d648ea04b"))
        # device that exists
        l = h.get_device_by_id("4d8b1d62-7921-4917-9b70-bbd31f6e2e8e")
        self.assertIsNotNone(l)
        self.assertEqual(l.id, "4d8b1d62-7921-4917-9b70-bbd31f6e2e8e")
        self.assertTrue(l in h.get_devices())


    # Level 2 Intermediate: Testing the attributes and methods of device object

    def test_intermediate_device_attributes(self):
        motion_sensor = h.get_device_by_id("cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5")
        self.assertEqual(motion_sensor.id, "cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5")
        self.assertEqual(motion_sensor.device_type, "Motion Sensor")
        self.assertEqual(motion_sensor.supplier, "NebulaGuard Innovations")
        self.assertEqual(motion_sensor.model_name, "MoveZ Detect 69")
        self.assertTrue(motion_sensor.is_sensor())
        self.assertFalse(motion_sensor.is_actuator())
        bulp = h.get_device_by_id("6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28")
        self.assertEqual(bulp.id, "6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28")
        self.assertEqual(bulp.device_type, "Light Bulp")
        self.assertEqual(bulp.supplier, "Elysian Tech")
        self.assertEqual(bulp.model_name, "Lumina Glow 4000")
        self.assertTrue(bulp.is_actuator())
        self.assertFalse(bulp.is_sensor())
        # also they know about their room and rooms know about their devices
        living_room = motion_sensor.room
        self.assertTrue(motion_sensor in living_room.devices)
        self.assertEqual(len(living_room.devices), 3)

    def test_intermediate_sensor_measurements(self):
        temp = h.get_device_by_id("4d8b1d62-7921-4917-9b70-bbd31f6e2e8e")
        m = temp.last_measurement()
        # Measurements are recorded in celsius and values a floating point numbers
        self.assertEqual(m.unit, "°C")
        self.assertEqual(type(m.value), type(0.0))

    def test_intermediate_actuator_state_change(self):
        # actuators can be turned on and off
        bulp = h.get_device_by_id("6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28")
        bulp.turn_on()
        self.assertTrue(bulp.is_active())
        bulp.turn_off()
        self.assertFalse(bulp.is_active())
        # some actuators can receive extra information
        heat_pump = h.get_device_by_id("5e13cabc-5c58-4bb3-82a2-3039e4480a6d")
        heat_pump.turn_on(21.3)
        self.assertTrue(heat_pump.is_active())
        heat_pump.turn_off()
        self.assertFalse(heat_pump.is_active())


    # Level 3 Advanced: Registering the same device in another room, moves it from one room to another 

    def test_zadvanced_move_device(self):
        # find the the dressing room
        dresser = None 
        for r in h.get_rooms():
            if r.room_name and r.room_name.lower().startswith("dress"):
                dresser = r 
                break
        self.assertIsNotNone(dresser)
        bulp = h.get_device_by_id("6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28")
        gr2 = bulp.room
        # before
        self.assertEqual(len(dresser.devices), 0)
        self.assertEqual(len(gr2.devices), 1)
        self.assertEqual(gr2, bulp.room)

        # moving the device 
        h.register_device(dresser, bulp)

        # after
        self.assertEqual(dresser, bulp.room)
        self.assertEqual(len(dresser.devices), 1)
        self.assertEqual(len(gr2.devices), 0)


if __name__ == "__main__":
    main()
