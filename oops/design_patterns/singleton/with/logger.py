class Logger:

    # def __init__(self):  # initialize the created object
    #     # attributes
    #     self.log_count = 0

    __instance = None;

    def __new__(cls):    # creates new object
        # return "hello"
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.log_count = 0

            return cls.__instance
        return cls.__instance

    def log(self, message):
        print(f"This is the log: {message}")
        self.log_count += 1

    def log_counter(self) -> int:
        return self.log_count
    

log1 = Logger()
log1.log("Hi") #count = 1
log2 = Logger()
log2.log("Bye") #count = 2
log3 = Logger()
log3.log("Bye 3") #count = 3
# print(id(log1), id(log2))

print(log1.log_counter())
print(log2.log_counter())
print(log3.log_counter())



# in python when we initialize any class it is going to create new object reference so we need to override it