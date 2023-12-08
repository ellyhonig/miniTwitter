import csv

class JobManager:
    def __init__(self, job_file='job_listings.csv', profile_manager=None):
        self.job_file = job_file
        self.profile_manager = profile_manager

    
    def get_all_jobs(self):
        jobs = []
        with open('job_listings.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                jobs.append(row)
        return jobs
    
    def post_job(self, author, message, user_type):
        if user_type == 'Surfer':
            return False, "Surfers cannot post job listings."
        elif user_type in ['TrendyUser', 'OrdinaryUser']:
            if self.profile_manager.get_balance(author) < 10:
                return False, "Insufficient balance to post job listing."
            self.profile_manager.update_balance(author, -10)
            self.profile_manager.add_warning(author, 'SuperUser')
        
        with open(self.job_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([author, message, ''])
        return True, "Job listing posted successfully."

    def apply(self, job_index, applicant):
        updated_listings = []
        success = False
        message = ""
        with open(self.job_file, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader) 
            for i, row in enumerate(reader, start=1):  
                print(f"Row {i}: {row}")  
                if len(row) < 3:
                    print(f"Skipping malformed row {i}: {row}")
                    continue
                if i == job_index+1:
                    if self.profile_manager.get_balance(row[1]) >= 0.1:
                        row[2] += f"{applicant},"
                        self.profile_manager.update_balance(row[1], -0.1)
                        self.profile_manager.update_balance('SuperUser', 0.1)
                        success = True
                        message = "Application successful."
                    else:
                        message = "Job poster has insufficient funds to accept applicants."
                updated_listings.append(row)

        if success:
            with open(self.job_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['author', 'message', 'applicants']) 
                writer.writerows(updated_listings)

        return success, message