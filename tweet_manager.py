import csv
from datetime import datetime

class TweetManager:
    def __init__(self, tweets_file='tweets.csv', taboo_file='taboo_words.csv', login_manager=None, warning_manager=None, profile_manager=None):
        self.tweets_file = tweets_file
        self.taboo_file = taboo_file
        self.login_manager = login_manager
        self.warning_manager = warning_manager
        self.profile_manager = profile_manager

    def post_tweet(self, content, keywords):
        if self.login_manager.current_user['user_type'] == 'Surfer':
            return False, "Surfers cannot post tweets."

        taboo_count, content = self.check_taboo_words(content)
        if taboo_count > 2:
            self.warning_manager.add_warning(self.login_manager.current_user['username'], 'System')
            return False, "Tweet contains too many taboo words and has been blocked."

        author = self.login_manager.current_user['username']
        time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%Y-%m-%d")
        views = 0
        complaints = 0
        comments = ""
        liker_list = ""
        dislikes = 0

        # Word count and billing logic
        word_count = len(content.split())
        user_balance = self.profile_manager.get_balance(author)
        cost = self.calculate_cost(word_count, self.login_manager.current_user['user_type'])

        if cost > user_balance:
            return False, "Insufficient balance to post tweet."

        # Deduct cost from user's balance
        self.profile_manager.update_balance(author, user_balance - cost)

        with open(self.tweets_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([author, time, date, keywords, views, complaints, comments, liker_list, dislikes, content])  
        return True, "Tweet posted successfully."

    def calculate_cost(self, word_count, user_type):
        if user_type == 'CorporateUser':
            return word_count * 1
        elif word_count > 20:
            return (word_count - 20) * 0.1
        return 0


    def check_taboo_words(self, content):
        taboo_words = self.get_taboo_words()
        word_list = content.split()
        taboo_count = 0

        for i, word in enumerate(word_list):
            if word.lower() in taboo_words:
                taboo_count += 1
                word_list[i] = '*' * len(word)

        return taboo_count, ' '.join(word_list)

    def get_taboo_words(self):
        taboo_words = set()
        with open(self.taboo_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                taboo_words.add(row[0].lower())
        return taboo_words
    def get_all_tweets(self):
        tweets = []
        with open(self.tweets_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tweets.append(row)
        return tweets
    def like_tweet(self, tweet_index, username):
        updated_tweets = []
        with open(self.tweets_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i == tweet_index:
                    likers = row['liker_list'].split(',')
                    if username not in likers:
                        row['liker_list'] += f"{username},"
                updated_tweets.append(row)

        with open(self.tweets_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(updated_tweets)

    def count_likes(self, liker_list):
        if not liker_list:
            return 0
        return len([liker for liker in liker_list.split(',') if liker])

    def dislike_tweet(self, tweet_index, username):
        # Logic to add a dislike to the tweet
        self.update_tweet_interaction(tweet_index, 'dislike', username)

    def complain_tweet(self, tweet_index):
        updated_tweets = []
        fieldnames = ['author', 'time', 'date', 'keyword_list', 'views', 'complaints', 'comments', 'liker_list', 'dislikes', 'content']  # Ensure these match the CSV columns exactly

        with open(self.tweets_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                updated_tweets.append(row)

        tweet_index = int(tweet_index)  # Convert tweet_index to integer
        if tweet_index < len(updated_tweets):
            updated_tweets[tweet_index]['complaints'] = str(int(updated_tweets[tweet_index].get('complaints', 0)) + 1)
            # Add a warning to the author of the tweet
            tweet_author = updated_tweets[tweet_index]['author']
            self.warning_manager.add_warning(tweet_author, self.login_manager.current_user['username'])

        with open(self.tweets_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for tweet in updated_tweets:
                # Ensure each dictionary has all the required fields
                tweet_row = {fieldname: tweet.get(fieldname, '') for fieldname in fieldnames}
                writer.writerow(tweet_row)


    def comment_tweet(self, tweet_index, comment, username):
        updated_tweets = []
        with open(self.tweets_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i == int(tweet_index):
                    row['comments'] = row['comments'] + f"{username}: {comment}\n"
                updated_tweets.append(row)

        with open(self.tweets_file, 'w', newline='') as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_tweets)

    def update_tweet_interaction(self, tweet_index, interaction_type, username, comment=None):
        updated_tweets = []
        with open(self.tweets_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i == tweet_index:
                    if interaction_type == 'like':
                        row['likes'] = str(int(row['likes']) + 1)
                        row['liker_list'] += f"{username},"
                    elif interaction_type == 'dislike':
                        row['dislikes'] = str(int(row['dislikes']) + 1)
                    elif interaction_type == 'complain':
                        row['complaints'] = str(int(row['complaints']) + 1)
                    elif interaction_type == 'comment':
                        row['comments'] += f"{username}: {comment}\n"
                updated_tweets.append(row)

        with open(self.tweets_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(updated_tweets)

    def get_tweet_author(self, tweet_index):
        with open(self.tweets_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i == tweet_index:
                    return row['author']
        return None
    

    def get_trendytweets(self):
        tweets = []
        with open(self.tweets_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.count_likes(row['liker_list']) - int(row['dislikes']) > 3:
                    tweets.append(row)
        return tweets
    
    def get_topthree(self):
        temp = []
        tweets = []
        with open(self.tweets_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                    row['likes'] = self.count_likes(row['liker_list'])
                    tweets.append(row)

        tweets = sorted(tweets, key=lambda x: x['likes'])
        
        tweets = tweets[-3:]

        temp = tweets[::-1]


      

        


        
      
        return temp