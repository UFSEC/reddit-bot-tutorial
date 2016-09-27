from bot import MonitorBot

USERNAME = 'ufsec-bot'
PASSWORD = '123456'

# Main method - Program begins here
if __name__ == '__main__':
    # Create array of subreddits you'd like to monitor
    subreddits = ['learnprogramming', 'python', 'learnpython', 'programming']

    # Create array of strings you want to look for
    words = ['python', 'beginner', 'programming']

    # Create instance of the bot.
    # Allows an optional paramater of a reddit username to send messages to
    bot = MonitorBot(subreddits, words)

    # Sign in to reddit in order to send messages
    bot.login_to_reddit(USERNAME, PASSWORD)

    # Start the bot
    bot.start()
