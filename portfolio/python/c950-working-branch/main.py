# StudentID: 011687882
import sys
import datetime
import csv
from hash_table import ChainingHashTable
from package import Package
from truck import Truck

def main():
    # main workflow of program
    # creates an instance of the ChainingHashTable
    hash_table = ChainingHashTable()
    # imports package data from \csv\package_data
    import_package_data("csv\\package_data.csv", hash_table)
    # imports distance data from \csv\distance_data
    distance_list = import_distance_data("csv\\distance_data.csv")
    # imports address data from \csv\address_data
    address_list = import_address_data("csv\\address_list.csv")

    # creates 3 arrays to hold the IDs of packages grouped by delivery
    # delivery2 is restricted to truck2, delivery3 holds all EOD packages
    delivery1 = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
    delivery2 = [3, 6, 18, 25, 27, 28, 32, 33, 35, 36, 38, 39]
    # address for package 9 isn't known until 10:20AM
    delivery3 = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 22, 23, 24, 26]

    # creates the first two truck objects using specific delivery arrays and start times
    truck1 = Truck(1, len(delivery1), datetime.timedelta(hours=8, minutes=0))
    # start truck2 at 9:05AM for "delayed on flight" and truck 2 package requirements
    truck2 = Truck(2, len(delivery2), datetime.timedelta(hours=9, minutes=5))

    # loads and delivers each delivery array
    load_packages(truck1, delivery1, hash_table)
    deliver_packages(truck1, address_list, distance_list)

    load_packages(truck2, delivery2, hash_table)
    deliver_packages(truck2, address_list, distance_list)

    # truck3 starts at 10:20 to accommodate package 9's address change at that time
    truck3 = Truck(3, len(delivery3), datetime.timedelta(hours=10, minutes=20))
    load_packages(truck3, delivery3, hash_table)
    # hub knows package 9's address by 10:20, sets directly while at hub then delivers
    truck3.package_list[5].address = "410 S State St"
    truck3.package_list[5].zip = "84111"
    deliver_packages(truck3, address_list, distance_list)

    # adds together the total mileage from each truck
    total_mileage = truck1.mileage + truck2.mileage + truck3.mileage

    # sets up the menu for user interaction
    menu(hash_table, total_mileage)

# imports csv data into the passed hash table object
# time complexity: O(N), space complexity: O(N)
def import_package_data(file, ht):
    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = int(row[4])
            deadline = row[5]
            weight = int(row[6])
            note = row[7]

            package = Package(package_id, address, city, state, zip_code, deadline, weight, note)
            ht.insert(package, package.id)

# imports distance data and returns a new list, requires distance_data file to be edited ahead of time
# time complexity: O(1), space complexity: O(1)
def import_distance_data(file):
    with open(file) as csv_file:
        dl = csv.reader(csv_file)
        return list(dl)

# imports address data and returns a new list, requires address_data file to be edited ahead of time
# time complexity: O(1), space complexity: O(1)
def import_address_data(file):
    with open(file) as csv_file:
        al = csv.reader(csv_file)
        return list(al)

# returns the distance between two values in the distance data list
# dl is main's distance_list, row/column for distance_list cells
# time complexity: O(1), space complexity: O(1)
def distance_between(dl, row, column):
    distance = dl[row][column]
    if distance == '':
        distance = dl[column][row]
    return float(distance)

# returns the index of the passed address from address_list, al is main's address_list
# address indexes need to be ints and will be used as row/column values for distance_between()
# time complexity: O(N), space complexity: O(N)
def address_index(al, address):
    for row in al:
        if address in row[2]:
            return int(row[0])

# uses a passed array to locate package objects based on ID
# directly assigns packages from ht into truck's package_list
# sets the truck number of each entry in package_list to truck.number
# time complexity: O(N), space complexity: O(N)
def load_packages(truck, delivery, ht):
    for i in range(len(delivery)):
        truck.package_list.append(ht.search(delivery[i]))
        truck.package_list[i].truck_number = truck.number

# creates a temporary array to hold the delivery list for each package
# searches through this temporary array for the next-closes package and adds it to the truck's package_list
# time complexity: O(N^2), space complexity: O(N)
def deliver_packages(truck, al, dl):
    # sets up a temporary array to hold packages for sorting
    temp = [Package] * len(truck.package_list)
    # adds each package object in package_list to temp array
    for i in range(len(temp)):
        temp[i] = truck.package_list[i]
    # clear the truck's unsorted package_list
    truck.package_list.clear()

    while len(temp) > 0:
        # set distance value to a large arbitrary float for initial comparison
        distance = 50.0
        # set next_package to None ahead of loop
        next_package = None
        # loops through temp array and finds next-closest package address
        for i in range(len(temp)):
            # if the distance between the next package and the current address is less than the current distance value,
            # set the distance to that value and save the package to be added next
            if distance_between(dl, address_index(al, truck.current_address), address_index(al, temp[i].address)) <= distance:
                distance = distance_between(dl, address_index(al, truck.current_address), address_index(al, temp[i].address))
                next_package = temp[i]
        # adds the next-closest package to the truck's package_list
        truck.package_list.append(next_package)
        # removes the next-closest package from temp
        if next_package in temp:
            temp.remove(next_package)
        else:
            break
        # adds the package distance value to the truck's mileage counter
        truck.mileage += distance
        # changes truck's current_address to next_package address
        truck.current_address = next_package.address
        # adds time required to deliver next-closest package to truck's current_time
        truck.current_time += datetime.timedelta(hours=(distance / 18))
        # updates delivery and departure times for the package
        next_package.deliver_time = truck.current_time
        next_package.depart_time = truck.depart_time
    # adds the distance between current address and the hub to mileage for return trip
    truck.mileage += distance_between(dl, address_index(al, truck.current_address), address_index(al, '4001 South 700 East'))

# calls get_status for a specific package id
# time complexity: O(1), space complexity: O(1)
def display_one_status(ht, id, time):
    package = ht.search(int(id))
    # ensure package 9 displays incorrect address if checked before 10:20AM
    if package.id == 9 and time < datetime.timedelta(hours=10, minutes=20):
        package.address = "300 State St"
        package.zip = "84103"
    # array of package IDs that have delayed arrival at the hub
    delays = [6, 25, 28, 32]
    # delayed packages do not arrive at hub until 9:05
    arrival = datetime.timedelta(hours=9, minutes=5)
    if package.id in delays and time < arrival:
        status = "is still in transit to the hub"
    elif package.deliver_time < time:
        status = "is delivered"
    elif package.depart_time < time < package.deliver_time:
        status = "is en route"
    else:
        status = "is at the hub"
    # print both generic package attributes and the status at the input time
    print(package)
    print("At " + str(time) + " package " + str(package.id) + " " + status)
    # line break for readability
    print("- - - - -")

# calls get_status for every package in the hash table
# time complexity: O(N), space complexity: O(N)
def display_all_status(ht, time):
    # search all package ids in the hash table
    for id in range(1, len(ht.table) + 1):
        package = ht.search(id)
        # get the status of the package at the specified time
        display_one_status(ht, id, time)

# converts an input string into a timedelta object2
# time complexity: O(1), space complexity: O(1)
def convert_input(input):
    (hour, minute, second) = input.split(":")
    hour = int(hour)
    minute = int(minute)
    second = int(second)
    return datetime.timedelta(hours=hour, minutes=minute, seconds=second)

# displays the menu for user interaction
def menu(ht, tm):
    # display the interactive menu
    print("++++++++++++++++++++++++++++++++++++++++++++")
    print("Western Governor's University Parcel Service")
    print("++++++++++++++++++++++++++++++++++++++++++++")
    print()
    print("To view the status of a package at a specific time, enter 1")
    print("To view the status of all packages at a specific time, enter 2")
    print("To view the total mileage of the trucks, enter 3")
    print("To quit, enter 4")
    print()
    selection = input("Please make a selection: ")
    match selection:
        case "1":
            print()
            time_input = input("Enter a time using the format HH:MM:SS: ")
            time = convert_input(time_input)
            id = input("Enter a package ID: ")
            display_one_status(ht, int(id), time)
        case "2":
            print()
            time_input = input("Enter a time using the format HH:MM:SS: ")
            time = convert_input(time_input)
            print("The status of all packages at time " + time_input + " :")
            display_all_status(ht, time)
        case "3":
            print()
            print("The total distance traveled for all trucks is: " + str(tm) + " miles")
        case "4":
            sys.exit()

if __name__ == "__main__":
    main()