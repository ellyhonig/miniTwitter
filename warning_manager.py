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

    def remove_warning(self, accused_user, accuser_user=None):
        updated_warnings = []
        with open(self.warnings_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
            #if no accuser given, remove any with accused. if accuser give, must match
                if not (row[0] == accused_user and (accuser_user is None or row[1] == accuser_user)):
                    updated_warnings.append(row)

        with open(self.warnings_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_warnings)

        with open(self.warnings_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_warnings)
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