import datetime

class Package:
    # set default address for all packages to the hub
    address = '4001 South 700 East'

    # parameterized constructor with variables for package attributes
    def __init__(self, package_id, address, city, state, zip, deadline, weight, note):
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.deliver_time = None
        self.depart_time = datetime.timedelta(hours=9, minutes=0, seconds=0)
        self.truck_number = 0

    # printed status requirements are ID, address, deadline, truck number, status, and deliver_time
    # truck number and status are determined and set in main()
    def __str__(self):
        return ('Package ID: %s, Delivery Address: %s, Delivery Deadline: %s, Truck Number: %s, Delivery Time: %s' %
                (self.id, self.address, self.deadline, self.truck_number, self.deliver_time))