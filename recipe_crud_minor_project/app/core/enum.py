from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class RecipeCategory(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    DESSERT = "dessert"
    SNACK = "snack"