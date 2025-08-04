import csv
from datetime import datetime

def save_test_drive(name, contact, date, time):
    with open("test_drive_bookings.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), name, contact, date, time])
