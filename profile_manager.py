import csv

class ProfileManager:
    def __init__(self, login_manager):
        self.login_manager = login_manager

    def add_profile(self, username, password, user_type, subscribers):
        with open('profiles.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password, user_type, subscribers])