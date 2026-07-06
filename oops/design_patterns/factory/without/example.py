from abc import ABC, abstractmethod

class Food(ABC):
    @abstractmethod
    def prepare():
        pass

class Pizza(Food):
    def prepare(self):
        print("Pizza preparing")

class Pasta(Food):
    def prepare(self):
        print("Pasta preparing")


# Consider this as client class- So adding new food item will also change this class so it violated openClose principle 
# hence we need Factory class which will only create object
class RestaurantService:
    def __init__(self, food):
        self.food = food
    
    def order_food(self):
        if self.food == "Pizza":
            p = Pizza()
            p.prepare()
            return p
        elif self.food == "Pasta":
            p = Pasta()
            p.prepare()
            return p
        else:
            return None


restaurant_service = RestaurantService("Pizza")
restaurant_service.order_food()
        

