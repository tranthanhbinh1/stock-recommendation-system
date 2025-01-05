import csv
import os
import random
from typing import Any, Callable

from faker import Faker
from faker.providers import BaseProvider


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


def generate_age():
    age = round(random.randint(18, 65))
    return age


def generate_income_and_assets():
    income = round(random.randint(1, 150) * 1e6, 2)
    # Calculate accumulated assets based on income
    # This is just a simple example; you can adjust the formula to make it more realistic
    accumulated_assets = income * random.uniform(1.5, 3)
    return [income, round(accumulated_assets, 2)]


def users_data_generator(fake: Faker) -> list[str]:
    return [
        fake.name(),
        generate_age(),
        *generate_income_and_assets(),
        fake.generate_goals(),
        fake.generate_risks(),
        fake.generate_experience(),
    ]


def generate_csv(
    filename: str,
    row_num: int,
    generator: Callable[[Faker], list[Any]],
    faker: Faker,
    header: list[str],
) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for n in range(1, row_num):
            writer.writerow(generator(faker))


if __name__ == "__main__":
    fake = Faker()
    fake.add_provider(InvestmentGoals)
    fake.add_provider(InvestmentExperience)
    fake.add_provider(RiskTolerance)

    for page in range(10):
        generate_csv(
            filename=f"data/user_data/user_data_{page}.csv",
            row_num=2000,
            generator=users_data_generator,
            faker=fake,
            header=[
                "Name",
                "Age",
                "Monthy Income",
                "Accumulated Assets",
                "Investment Goals",
                "Risk Tolerance",
                "Investment Experience",
            ],
        )
