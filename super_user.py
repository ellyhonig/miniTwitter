import csv
import os

class SuperUser:
    def __init__(self, profile_manager,application_manager):
        self.application_manager = application_manager
        self.profile_manager = profile_manager
        self.ensure_super_user_exists()

    def ensure_super_user_exists(self):
        profiles_file = 'profiles.csv'
        super_user_exists = False

        if os.path.exists(profiles_file):
            with open(profiles_file, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[2] == 'SuperUser':  
                        super_user_exists = True
                        break

        if not super_user_exists:
          
            self.profile_manager.add_profile('superuser', 'superuser_pass', 'SuperUser', '0')

    def add_profile(self, username, password, user_type, subscribers):
        return self.profile_manager.add_profile(username, password, user_type, subscribers)
    def manage_application(self, username, accept, rejection_reason='', temp_password=''):
        if accept:
            self.add_profile(username, temp_password, 'OrdinaryUser', '0')
            self.application_manager.update_application(username, 'Accepted', temp_password=temp_password)
        else:
            self.application_manager.update_application(username, 'Rejected', rejection_reason=rejection_reason)    
    def delete_user(self, username):
        self.profile_manager.delete_profile(username)        