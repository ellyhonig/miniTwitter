import csv

class ProfileManager:
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def add_profile(self, username, password, user_type, subscribers):
        with open('profiles.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password, user_type, subscribers])
    def delete_profile(self, username):
        updated_profiles = []
        with open('profiles.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != username:
                    updated_profiles.append(row)

        with open('profiles.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_profiles)

    def get_all_profiles(self):
        profiles = []
        with open('profiles.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                profiles.append(row)
        return profiles        