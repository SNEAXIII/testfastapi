from datetime import datetime
LOG_PATH = "./logs/logs"

class MiniLog:
    def __init__(self):
        self.log("___________________\nSession initialized", display_date=False)

    @staticmethod
    def log(message, display_date=True):
        print(message)
        date = ""
        if display_date:
            date = f"{datetime.now()} ---- "
        with open(LOG_PATH, "a") as f:
            f.write(f"{date}{message}\n")

    @staticmethod
    def clear_log():
        with open(LOG_PATH, "w") as f:
            return

    @staticmethod
    def get_log():
        with open(LOG_PATH) as f:
            return f.readlines()


ml = MiniLog()
