from smarthouse.domain import SmartHouse, Aktuator, Sensor

DEMO_HOUSE = SmartHouse()

# Building house structure
ground_floor = DEMO_HOUSE.register_floor(1)
second_floor = DEMO_HOUSE.register_floor(2)

entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
guest_room = DEMO_HOUSE.register_room(ground_floor, 8, "Guest room")
bathroom = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom")
livingRoom_Kitchen = DEMO_HOUSE.register_room(ground_floor, 39.75, "LivingRoom / Kitchen")
garage = DEMO_HOUSE.register_room(ground_floor, 19, "Garage")

office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
bathroom_2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom 2")
guest_room_2 = DEMO_HOUSE.register_room(second_floor, 8, "Guest Room 2")
guest_room_3 = DEMO_HOUSE.register_room(second_floor, 10, "Dressing Room")
dressing_room = DEMO_HOUSE.register_room(second_floor, 4, "Office")
master_bedroom = DEMO_HOUSE.register_room(second_floor, 17, "Master Bedroom")

smart_lock = DEMO_HOUSE.register_device(entrance, Aktuator("4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", "MythicalTech", "Guardian Lock 7000", "Smart Lock"))
smart_oven = DEMO_HOUSE.register_device(guest_room, Aktuator("8d4e4c98-21a9-4d1e-bf18-523285ad90f6","AetherCorp","Pheonix HEAT 333","Smart Oven"))
heat_pump = DEMO_HOUSE.register_device(livingRoom_Kitchen, Aktuator("5e13cabc-5c58-4bb3-82a2-3039e4480a6d","ElysianTech","Thermo Smart 6000","Heat Pump"))
electricity_meter = DEMO_HOUSE.register_device(entrance, Sensor("a2f8690f-2b3a-43cd-90b8-9deea98b42a7","MysticEnergy Innovations","Volt Watch Elite","V","Electricity Meter"))
humidity_sensor = DEMO_HOUSE.register_device(bathroom, Sensor("3d87e5c0-8716-4b0b-9c67-087eaaed7b45","AetherCorp","	Aqua Alert 800","%","Humidity Sensor"))
motion_sensor = DEMO_HOUSE.register_device(livingRoom_Kitchen, Sensor("cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5","NebulaGuard Innovations","MoveZ Detect 69","","Motion Sensor"))
co2_sensor = DEMO_HOUSE.register_device(livingRoom_Kitchen, Sensor("8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e","ElysianTech","Smoke Warden 1000","%","CO2 sensor"))
garage_door = DEMO_HOUSE.register_device(garage, Aktuator("9a54c1ec-0cb5-45a7-b20d-2a7349f1b132","MythicalTech","Guardian Lock 9000","Automatic Garage Door"))

lightbulp = DEMO_HOUSE.register_device(guest_room_2, Aktuator("6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28","Elysian Tech","Lumina Glow 4000","Light Bulp"))
smart_oven_2 = DEMO_HOUSE.register_device(master_bedroom, Aktuator("c1e8fa9c-4b8d-487a-a1a5-2b148ee9d2d1","IgnisTech Solutions","Ember Heat 3000","Smart Oven"))
temperatur_sensor = DEMO_HOUSE.register_device(master_bedroom, Sensor("4d8b1d62-7921-4917-9b70-bbd31f6e2e8e","AetherCorp","SmartTemp 42","celcius degree","Temperature Sensor"))
air_sensor = DEMO_HOUSE.register_device(guest_room_3, Sensor("7c6e35e1-2d8b-4d81-a586-5d01a03bb02c","CelestialSense Technologies","AeroGuard Pro","","Air Quality Sensor"))
smart_plug = DEMO_HOUSE.register_device(office, Aktuator("1a66c3d6-22b2-446e-bf5c-eb5b9d1a8c79","MysticEnergy Innovations","FlowState X","Smart Plug"))
dehumidifier = DEMO_HOUSE.register_device(bathroom_2, Aktuator("9e5b8274-4e77-4e4e-80d2-b40d648ea02a","ArcaneTech Solutions","Hydra Dry 8000","Dehumidifier"))
