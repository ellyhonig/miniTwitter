import csv

class Surfer:
    def submit_application(self, desired_username):
        with open('registration.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([desired_username])
