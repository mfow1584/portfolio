class Truck:
    def __init__(self, number, inventory, depart_time):
        # package_list set as an array of Package objects with length 'inventory'
        self.package_list = [] * inventory
        self.mileage = 0.0
        self.speed = 18
        self.start_address = '4001 South 700 East'
        self.current_address = '4001 South 700 East'
        self.current_time = depart_time
        self.depart_time = depart_time
        self.number = number