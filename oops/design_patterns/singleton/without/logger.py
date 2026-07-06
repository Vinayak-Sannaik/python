class Logger:

    def __init__(self):
        # attributes
        self.log_count = 0

    def log(self, message):
        print(f"This is the log: {message}")
        self.log_count += 1

    def log_counter(self) -> int:
        return self.log_count
    

log1 = Logger()
log1.log("Hi")
log2 = Logger()
log2.log("Bye")


print(log2.log_counter())


# here if we are seeing count always 1 because log2 is creating new object and for logging so this is problem
#  we need global centralized counter to count all logs count.



