from abc import ABC, abstractmethod

class Food(ABC):
    @abstractmethod
    def prepare(self):
        pass

class Pizza(Food):
    def prepare(self):
        print("Pizza preparing")

class Pasta(Food):
    def prepare(self):
        print("Pasta preparing")

class Chai(Food):
    def prepare(self):
        print("Chai preparing")


# Consider this as client class- So adding new food item will also change this class so it violated openClose principle 
# hence we need Factory class which will only create object


from enum import Enum

class FoodType(Enum):
    PIZZA = "Pizza"
    PASTA = "Pasta"
    CHAI = "Chai"

# Factory should only create objects
class FoodFactory:
    def __init__(self):
        pass
        
    # it will not take self
    @staticmethod
    def create_food(food):
        if food == FoodType.PIZZA:
            p = Pizza()
            # p.prepare(). this is wrong because factory only creates object not include business logic
        elif food == FoodType.PASTA:
            p = Pasta()
        elif food == FoodType.CHAI:
            p = Chai()
        else:
            return None

        return p
    

class RestaurantService:
    def __init__(self, food):
        self.food = food
    
    def order_food(self):

        # we need initialize and call but if we use static we can call method directly
        # p = FoodFactory(self.food)
        # p.create_food()

        p = FoodFactory.create_food(self.food)
        if p == None:
            print("not available")

        p.prepare()
        # if self.food == "Pizza":
        #     p = Pizza()
        #     p.prepare()
        #     return p
        # elif self.food == "Pasta":
        #     p = Pasta()
        #     p.prepare()
        #     return p
        # else:
        #     return None


restaurant_service = RestaurantService(FoodType.PIZZA)
restaurant_service.order_food()



# Refactored factory class

# class FoodFactory:

#     food_map = {
#         FoodType.PIZZA: Pizza,
#         FoodType.PASTA: Pasta,
#         FoodType.CHAI: Chai,
#     }

#     @staticmethod
#     def create_food(food):
#         food_class = FoodFactory.food_map.get(food)

#         if food_class is None:
#             return None

#         return food_class()
    

        

