import csv

class WarningManager:
    def __init__(self, warnings_file='warnings.csv'):
        self.warnings_file = warnings_file

    def get_disputed_warnings(self):
        disputed_warnings = []
        with open(self.warnings_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[2] == 'true':  #  disputed is the third column
                    disputed_warnings.append(row)
        return disputed_warnings
    def get_user_warnings(self, username):
        user_warnings = []
        with open(self.warnings_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['accused_user'] == username and row['disputed'] == 'false':
                    user_warnings.append(row)
        return user_warnings
    def remove_warning(self, accused_user, accuser_user=None):
        updated_warnings = []
        with open(self.warnings_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
            #if no accuser given, remove any with accused. if accuser give, must match
                if not (row[0] == accused_user and (accuser_user is None or row[1] == accuser_user)):
                    updated_warnings.append(row)
    def dispute_warning(self, username, warning_index):
        updated_warnings = []
        success = False
        with open(self.warnings_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if row['accused_user'] == username :
                    row['disputed'] = 'true'
                    success = True
                updated_warnings.append(row)

        if success:
            with open(self.warnings_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(updated_warnings)
            return True, "Warning successfully disputed."
        else:
            return False, "Failed to dispute warning."

    def add_warning(self, accused_user, accuser_user, disputed='false'):
        with open(self.warnings_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([accused_user, accuser_user, disputed])
    def count_warnings(self, username):
        count = 0
        with open(self.warnings_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:  # accused_user is first column
                    count += 1
        return count
    def remove_all_warnings(self, username):
        while self.count_warnings(username) > 0:
            self.remove_warning(username, None)                     