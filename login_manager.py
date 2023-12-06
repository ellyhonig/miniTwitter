import csv

class LoginManager:
    def __init__(self):
        self.current_user = {'username': None, 'user_type': 'Surfer'}

    def login(self, username, password):
        #check username and password
        with open('profiles.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username and row[1] == password:
                    self.current_user['username'] = username
                    self.current_user['user_type'] = row[2]  # Assuming user type is in the third column
                    return "Login successful", True
        return "Username or password incorrect", False