import datetime
from enum import Enum

import pytest

from meal_planner import meal_plan_generator
from meal_planner.mealitem import MealItem
from meal_planner.plan_period import PlanPeriod


def test_generate_meal_plan_happy_day():
    test_meals_names = ["Steak", "Bolognese", "Funky meal", "Jazzy meal"]

    meals_list: list[MealItem] = []
    steak = MealItem(test_meals_names[0], 1, None)
    meals_list.append(steak)
    steak = MealItem(test_meals_names[1], 3, None)
    meals_list.append(steak)
    funky = MealItem(test_meals_names[2], 3, None)
    meals_list.append(funky)
    jazzy = MealItem(test_meals_names[3], 3, None)
    meals_list.append(jazzy)

    test_meal_plan = meal_plan_generator.generate_meal_plan(
        meals_list, PlanPeriod.NEXT_WEEK, datetime.date(2021, 11, 11), 14
    )

    assert len(meals_list) == 4, "should not remove items from the original list"
    assert steak in meals_list, "should not remove items from the original list"
    assert funky in meals_list, "should not remove items from the original list"
    assert jazzy in meals_list, "should not remove items from the original list"

    sum_days: int = 0
    for meal in test_meal_plan:
        sum_days += meal.days_to_serve
        assert meal.name in test_meals_names, "Only meals from menu are to be used"

    assert sum_days >= 7, "At least 7 days must be covered"
    assert sum_days == sum(m.days_to_serve for m in test_meal_plan)
    assert (
        sum(m.last_suggested == datetime.date(2021, 11, 15) for m in test_meal_plan)
        == 1
    ), "There should be one meal for the Monday following the 11.11.2021"


def test_generate_meal_plan_period_from_last_suggested():

    meals_list: list[MealItem] = []
    steak = MealItem(
        "Steak not suggested for long time",
        1,
        datetime.date.fromisoformat("2021-10-20"),
    )
    meals_list.append(steak)
    jazzy = MealItem(
        "Jazzy meal suggested recently", 3, datetime.date.fromisoformat("2021-11-10")
    )
    meals_list.append(jazzy)

    test_meal_plan = meal_plan_generator.generate_meal_plan(
        meals_list, PlanPeriod.TOMORROW, datetime.date(2021, 11, 11), 14
    )

    assert (
        sum(m.name == "Jazzy meal suggested recently" for m in test_meal_plan) == 0
    ), "Meal suggested in last 14 days (constant DAYS_MEAL_MUST_NOT_BE_SUGGESTED in main.py) must not be chosen"


class PlanPeriodWrong(str, Enum):
    # since the most important recipient of meal plan is not proficient enough in English values are in Czech
    YESTERDAY = "včera"


def test_generate_meal_plan_should_raise_index_exc():
    meals_list: list[MealItem] = []

    with pytest.raises(IndexError):
        meal_plan_generator.generate_meal_plan(
            meals_list, PlanPeriodWrong.YESTERDAY, datetime.date.today(), 14
        )
