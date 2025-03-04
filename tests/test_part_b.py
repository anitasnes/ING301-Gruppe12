import unittest

from pathlib import Path
import sys 
sys.path.append(str(Path().parent.absolute()))

from smarthouse.persistence import SmartHouseRepository

class SmartHouseTest(unittest.TestCase):
    file = Path(__file__).parent / "../data/db.sql"
    repo = SmartHouseRepository(file)

    def test_cursor(self):
        c = self.repo.cursor()
        c.execute("SELECT * FROM rooms")
        rooms = c.fetchall()
        self.assertEqual(12, len(rooms))
        c.close()

    # Testing that the device structure is loaded correctly

    def test_basic_no_of_rooms(self):
        h = self.repo.load_smarthouse_deep()
        self.assertEqual(len(h.get_rooms()), 12)

    def test_basic_get_area_size(self):
        h = self.repo.load_smarthouse_deep()
        self.assertEqual(h.get_area(), 156.55)

    def test_basic_get_no_of_devices(self):
        h = self.repo.load_smarthouse_deep()
        self.assertEqual(len(h.get_devices()), 14)


    def test_basic_read_values(self):
        h = self.repo.load_smarthouse_deep()
        actuator = h.get_device_by_id("9a54c1ec-0cb5-45a7-b20d-2a7349f1b132")
        motion_sensor = h.get_device_by_id("cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5")
        amp_sensor = h.get_device_by_id("a2f8690f-2b3a-43cd-90b8-9deea98b42a7")
        humidity_sensor = h.get_device_by_id("3d87e5c0-8716-4b0b-9c67-087eaaed7b45")
        # is not even a sensor
        self.assertEqual(None, self.repo.get_latest_reading(actuator))
        # data exists
        self.assertEqual(13.7, self.repo.get_latest_reading(amp_sensor).value)
        self.assertEqual('2024-01-28 23:00:00', self.repo.get_latest_reading(amp_sensor).timestamp)
        # has no data
        self.assertEqual(None, self.repo.get_latest_reading(motion_sensor))
        # data exists
        self.assertEqual(55.2125, self.repo.get_latest_reading(humidity_sensor).value)
        self.assertEqual('2024-01-29 16:00:01', self.repo.get_latest_reading(humidity_sensor).timestamp)


    def test_intermediate_save_actuator_state(self):
        h = self.repo.load_smarthouse_deep()
        oven = h.get_device_by_id("8d4e4c98-21a9-4d1e-bf18-523285ad90f6")
        plug = h.get_device_by_id("1a66c3d6-22b2-446e-bf5c-eb5b9d1a8c79")
        oven.turn_on(24.0)
        plug.turn_on()
        self.repo.update_actuator_state(oven)
        self.repo.update_actuator_state(plug)
        self.assertTrue(oven.is_active())
        self.assertTrue(plug.is_active())
        # first reconnect
        self.repo.reconnect()
        h = self.repo.load_smarthouse_deep()
        oven = h.get_device_by_id("8d4e4c98-21a9-4d1e-bf18-523285ad90f6")
        plug = h.get_device_by_id("1a66c3d6-22b2-446e-bf5c-eb5b9d1a8c79")
        # activation should have been persisted
        self.assertTrue(oven.is_active())
        self.assertTrue(plug.is_active())
        # turning them off again
        oven.turn_off()
        plug.turn_off()
        self.repo.update_actuator_state(oven)
        self.repo.update_actuator_state(plug)
        self.assertFalse(oven.is_active())
        self.assertFalse(plug.is_active())
        # second reconnect
        self.repo.reconnect()
        h = self.repo.load_smarthouse_deep()
        oven = h.get_device_by_id("8d4e4c98-21a9-4d1e-bf18-523285ad90f6")
        plug = h.get_device_by_id("1a66c3d6-22b2-446e-bf5c-eb5b9d1a8c79")
        # deactivation should have been persisted
        self.assertFalse(oven.is_active())
        self.assertFalse(plug.is_active())
        
        
    def test_zadvanced_test_humidity_hours(self):
        bath = None 
        h = self.repo.load_smarthouse_deep()
        for r in h.get_rooms():
            if "bath" in r.room_name.lower() and "1" in r.room_name.lower():
                bath = r 
                break

        expected = [7, 8, 9, 12, 18]
        result = self.repo.calc_hours_with_humidity_above(bath, '2024-01-27')
        self.assertSetEqual(set(expected), set(result))


    def test_zadvanced_test_temp_avgs(self):
        living_room = None
        garage = None
        bedroom = None

        h = self.repo.load_smarthouse_deep()
        for r in h.get_rooms():
            if "kitchen" in r.room_name.lower():
                living_room = r 
            if "bedroom" in r.room_name.lower():
                bedroom = r 
            if "garage" in r.room_name.lower():
                garage = r
            if living_room and garage and bedroom:
                break

        expected1 = {
            '2024-01-27': 21.9167,
            '2024-01-28': 19.0444
        }
        actual1 = self.repo.calc_avg_temperatures_in_room(bedroom, '2024-01-27', None)
        self.assertEqual(expected1.keys(), actual1.keys())
        for k in expected1.keys():
            self.assertAlmostEqual(actual1[k], expected1[k], 3)

        actual2 = self.repo.calc_avg_temperatures_in_room(garage, '2024-01-15', '2024-01-28')
        self.assertEqual({}, actual2)


        expected3 = {
            '2024-01-24': 20.9167,
            '2024-01-25': 21.9167,
            '2024-01-26': 22.9167
        }
        actual3 = self.repo.calc_avg_temperatures_in_room(living_room, None, '2024-01-26')
        self.assertEqual(expected3.keys(), actual3.keys())
        for k in expected3.keys():
            self.assertAlmostEqual(expected3[k], actual3[k], 3)




if __name__ == '__main__':
    unittest.main()
