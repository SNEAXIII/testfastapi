from datetime import datetime


class MiniLog:
    def __init__(self):
        self.log("___________________\nSession initialized", display_date=False)

    @staticmethod
    def log(message, display_date=True):
        print(message)
        date = ""
        if display_date:
            date = f"{datetime.now()} ---- "
        with open("logged", "a") as f:
            f.write(f"{date}{message}\n")

    @staticmethod
    def clear_log():
        with open("logged", "w") as f:
            return

    @staticmethod
    def get_log():
        with open("logged") as f:
            return f.read()


ml = MiniLog()
