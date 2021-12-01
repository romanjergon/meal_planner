import datetime
import random
from calendar import monthrange

from dateutil.relativedelta import relativedelta

from meal_planner.mealitem import MealItem
from meal_planner.plan_period import PlanPeriod


def get_num_days(plan_period: PlanPeriod, create_date: datetime.date) -> int:
    if plan_period.value in [PlanPeriod.TODAY.value, PlanPeriod.TOMORROW.value]:
        return 1
    elif plan_period.value == PlanPeriod.NEXT_WEEK.value:
        return 7
    elif plan_period.value == PlanPeriod.NEXT_MONTH.value:
        next_month: datetime.date = datetime.date(
            create_date.year, create_date.month, 1
        ) + relativedelta(months=1)
        return monthrange(next_month.year, next_month.month)[1]

    else:
        raise IndexError(f"Wrong period value {plan_period}")


def get_period_start(
    plan_period: PlanPeriod, create_date: datetime.date
) -> datetime.date:
    if plan_period.value == PlanPeriod.TODAY.value:
        return create_date

    elif plan_period.value == PlanPeriod.TOMORROW.value:
        return create_date + datetime.timedelta(days=1)

    elif plan_period.value == PlanPeriod.NEXT_WEEK.value:
        index_of_day = create_date.weekday()
        next_monday = create_date + datetime.timedelta(days=7 - index_of_day)
        return next_monday

    elif plan_period.value == PlanPeriod.NEXT_MONTH.value:
        next_month_start: datetime.date = datetime.date(
            create_date.year, create_date.month, 1
        ) + relativedelta(months=1)
        return next_month_start
    else:
        raise IndexError(f"Wrong period value {plan_period}")


def remove_recently_suggested(
    meals_list: list[MealItem],
    period_start: datetime.date,
    days_meal_should_not_be_suggested: int,
) -> list[MealItem]:
    init_working_meals_list = meals_list.copy()
    # keep meals that were not suggested at least number of days_meal_should_not_be_suggested before period_start
    meals_remaining = []
    for meal in init_working_meals_list:
        if meal.last_suggested is None:
            meals_remaining.append(meal)
        elif (
            meal.last_suggested
            + datetime.timedelta(days=days_meal_should_not_be_suggested)
            <= period_start
        ):
            meals_remaining.append(meal)
    return meals_remaining


def select_meals(
    meals_list: list[MealItem],
    num_days: int,
    period_start: datetime.date,
    days_meal_should_not_be_suggested: int,
) -> list[MealItem]:
    working_meals_list: list[MealItem] = remove_recently_suggested(
        meals_list, period_start, days_meal_should_not_be_suggested
    )
    selected_meals: list[MealItem] = []
    days_remaining: int = num_days
    cooking_day = period_start
    while days_remaining > 0 and len(working_meals_list) > 0:
        chosen_meal = random.choice(working_meals_list)
        new_meal = MealItem(chosen_meal.name, chosen_meal.days_to_serve, cooking_day)
        selected_meals.append(new_meal)
        days_remaining -= new_meal.days_to_serve
        cooking_day += datetime.timedelta(days=new_meal.days_to_serve)
        working_meals_list.remove(chosen_meal)
    return selected_meals


def generate_meal_plan(
    meals_list: list[MealItem],
    plan_period: PlanPeriod,
    create_date: datetime.date,
    days_meal_should_not_be_suggested: int,
) -> list[MealItem]:
    # get number of days to plan from period
    number_days: int = get_num_days(plan_period, create_date)
    # generate end and start date from period
    period_start: datetime.date = get_period_start(plan_period, create_date)
    # select meals from the list to cover the number of days
    meals_plan: list[MealItem] = select_meals(
        meals_list, number_days, period_start, days_meal_should_not_be_suggested
    )
    return meals_plan
