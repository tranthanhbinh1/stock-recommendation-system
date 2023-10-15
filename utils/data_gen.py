from faker import Faker
from faker.providers import BaseProvider
import random
from typing import Any


class InvestmentGoals(BaseProvider):
    def generate_goals(self) -> str:
        goals = ["Short-term", "Medium-term", "Long-term"]
        return random.choice(goals)
    
class RiskTolerance(BaseProvider):
    def generate_risks(self) -> str:
        risks = ["low", "medium", "high"]
        return random.choice(risks) 
    
class InvestmentExperience(BaseProvider):
    def generate_experience(self) -> str:
        experiences = [f"Under {number} year" for number in range(10)]
        return random.choice(experiences)
        
def generate_income_and_assets():
    # Generate random monthly income between $1,000 and $10,000
    income = round(random.randint(1, 10)* 1e6, 2)
    # Calculate accumulated assets based on income
    # This is just a simple example; you can adjust the formula to make it more realistic
    accumulated_assets = income * random.uniform(1.5, 3)
    return income, round(accumulated_assets, 2)


print(generate_income_and_assets())