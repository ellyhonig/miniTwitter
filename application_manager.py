import csv

class ApplicationManager:
    def __init__(self, registration_file='registration.csv'):
        self.registration_file = registration_file

    def get_applications(self):
        applications = []
        with open(self.registration_file, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header
            for row in reader:
                applications.append(row)
        return applications

    def update_application(self, username, status, rejection_reason='', temp_password=''):
        updated_rows = []
        with open(self.registration_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    row[2] = status
                    row[3] = rejection_reason
                    row[4] = temp_password
                updated_rows.append(row)

        with open(self.registration_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
