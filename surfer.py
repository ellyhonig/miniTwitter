import csv

class Surfer:
    def submit_application(self, desired_username, user_type):
        with open('registration.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Write username, user type, and leave other fields blank
            writer.writerow([desired_username, user_type, '', '', ''])
    def check_application_status(self, username):
        with open('registration.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    # Return status, rejection reason, and temp password
                    return row[2], row[3], row[4]
        return 'Not Found', '', ''        