class MiniLog:
    def __init__(self):
        self.log("___________________\nSession initialized")

    @staticmethod
    def log(message):
        with open("logged", "a") as f:
            f.write(message)
            print(message)
