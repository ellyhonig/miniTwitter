import csv

class ProfileManager:
    def __init__(self, login_manager):
        self.login_manager = login_manager
    
    def add_profile(self, username, password, user_type, subscribers, balance=0):
        with open('profiles.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password, user_type, subscribers, balance])
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
    def get_profile_info(self, username, warning_manager):
        profile_info = {}
        with open('profiles.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    profile_info = {
                        'username': row['username'],
                        'password': row['password'],
                        'balance': row['balence'],  # Update this line
                        'subscribers': row['subscribers'],
                        'warnings': warning_manager.count_warnings(username),
                        'user_type': row['user_type']
                    }
                    break
        return profile_info

    def get_all_profiles(self):
        profiles = []
        with open('profiles.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                profiles.append(row)
        return profiles        
    def get_user_type(self, username):
        with open('profiles.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    return row[2]  
        return None
    def add_subscribers(self, username, additional_subscribers):
        updated_profiles = []
        subscriber_index = 4  
        print('subs added')
        with open('profiles.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    current_subscribers = int(row[subscriber_index])
                    row[subscriber_index] = str(current_subscribers + additional_subscribers)
                updated_profiles.append(row)

        with open('profiles.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_profiles)    
    def change_password(self, username, new_password):
        updated_rows = []
        with open('profiles.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:  
                    row[1] = new_password  
                updated_rows.append(row)

        with open('profiles.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
    def update_balance(self, username, amount, add=True):
        current_balance = self.get_balance(username)
        new_balance = current_balance + amount if add else current_balance - amount

        updated_profiles = []
        with open('profiles.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    row[4] = str(new_balance) 
                updated_profiles.append(row)

        with open('profiles.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_profiles)
       
    def get_balance(self, username):
        with open('profiles.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    return float(row[4])  
        return 0  # ret 0 if user not found
    
    def tip_user(self, tipper_username, recipient_username, amount):
        if self.get_balance(tipper_username) < amount:
            return False, "Insufficient balance to tip."

        self.update_balance(tipper_username, amount, add=False)
        self.update_balance(recipient_username, amount, add=True)
        return True, "Tip successful."    
