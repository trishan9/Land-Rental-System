import os
from datetime import datetime

LAND_DATA_FILE = "land_data.txt"
TRANSACTION_LOG_FILE = "transaction_log.txt"
INVOICE_DIRECTORY = "invoices"


def read_land_data():
    land_data = {}
    with open(LAND_DATA_FILE, "r") as file:
        for line in file:
            kitta, city, direction, area, price, status = line.strip().split(", ")
            land_data[kitta] = {"city": city, "direction": direction, "area": area, "price": price, "status": status}
    return land_data


def update_land_status(land_data, kitta, status):
    land_data[kitta]["status"] = status
    with open(LAND_DATA_FILE, "w") as file:
        for kitta, info in land_data.items():
            file.write(
                f"{kitta}, {info['city']}, {info['direction']}, {info['area']}, {info['price']}, {info['status']}\n")


def generate_invoice(transaction_type, kitta, city, direction, area, customer_name, date_time, duration, total_amount):
    invoice_dir = os.path.join(os.getcwd(), INVOICE_DIRECTORY)
    if not os.path.exists(invoice_dir):
        os.makedirs(invoice_dir)
    invoice_file = os.path.join(invoice_dir,
                                f"{transaction_type}_{customer_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
    with open(invoice_file, "w") as file:
        file.write(
            f"Kitta Number: {kitta}\nCity/District: {city}\nDirection: {direction}\nArea: {area} anna\nCustomer Name: {customer_name}\nDate and Time: {date_time}\nDuration: {duration} months\nTotal Amount: {total_amount}\n")


def rent_land(land_data, kitta, customer_name, duration):
    if land_data[kitta]["status"] == "Available":
        land_data[kitta]["status"] = "Not Available"
        update_land_status(land_data, kitta, "Not Available")
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_amount = int(land_data[kitta]["price"]) * duration
        generate_invoice("rent", kitta, land_data[kitta]["city"], land_data[kitta]["direction"],
                         land_data[kitta]["area"], customer_name, date_time, duration, total_amount)
        print(f"Land {kitta} rented successfully to {customer_name}.")
    else:
        print(f"Land {kitta} is not available for rent.")


def return_land(land_data, kitta, customer_name, duration):
    if land_data[kitta]["status"] == "Not Available":
        land_data[kitta]["status"] = "Available"
        update_land_status(land_data, kitta, "Available")
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_amount = int(land_data[kitta]["price"]) * duration
        generate_invoice("return", kitta, land_data[kitta]["city"], land_data[kitta]["direction"],
                         land_data[kitta]["area"], customer_name, date_time, duration, total_amount)
        print(f"Land {kitta} returned successfully by {customer_name}.")
    else:
        print(f"Land {kitta} is already available.")


def main():
    land_data = read_land_data()

    while True:
        print("\n1. Rent Land\n2. Return Land\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            kitta = input("Enter the kitta number of the land to rent: ")
            customer_name = input("Enter your name: ")
            duration = int(input("Enter the duration of rent (in months): "))
            rent_land(land_data, kitta, customer_name, duration)
        elif choice == "2":
            kitta = input("Enter the kitta number of the land to return: ")
            customer_name = input("Enter your name: ")
            duration = int(input("Enter the duration of rent (in months): "))
            return_land(land_data, kitta, customer_name, duration)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
