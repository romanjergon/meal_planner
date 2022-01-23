import argparse
import datetime
import logging
import os

from meal_planner import meal_plan_formatter
from meal_planner import meal_plan_generator
from dotenv import load_dotenv
from meal_planner.meals_list_manager import MealsListManager
from meal_planner.plan_period import PlanPeriod

import meal_planner.mail_notifier
from meal_planner.mealitem import MealItem

load_dotenv()


def get_plan_period(default_plan_period: PlanPeriod) -> PlanPeriod:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--plan_period",
        help="Sets the plan period for the meal plan. Valid values: TODAY, TOMORROW, NEXT_WEEK, NEXT_MOTH. Default value is NEXT_WEEK.",
        default=f"{default_plan_period.name}",
    )
    args = parser.parse_args()
    plan_period = default_plan_period
    if args.plan_period:
        if PlanPeriod.TODAY.name == args.plan_period:
            plan_period = PlanPeriod.TODAY
        elif PlanPeriod.TOMORROW.name == args.plan_period:
            plan_period = PlanPeriod.TOMORROW
        elif PlanPeriod.NEXT_WEEK.name == args.plan_period:
            plan_period = PlanPeriod.NEXT_WEEK
        elif PlanPeriod.NEXT_MONTH.name == args.plan_period:
            plan_period = PlanPeriod.NEXT_MONTH
        else:
            raise ValueError("Wrong plan_period value")

    return plan_period


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s"
    )
    # region constants
    DEFAULT_PLAN_PERIOD = PlanPeriod.NEXT_WEEK
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    SPREDSHEET_TITLE = "Recepty we like"
    WORKSHEET_INDEX = 0
    GOOGLE_ACCOUNT_CREDENTIALS_ENV_VAR = "GOOGLE_CREDENTIALS"
    DAYS_MEAL_MUST_NOT_BE_SUGGESTED = 14
    # endregion

    # region env vars
    notification_mailbox = os.environ["NOTIFICATION_MAILBOX"]
    mail_password = os.environ["MAIL_PASSWORD"]
    personal_mailbox = os.environ["PERSONAL_MAILBOX"]
    meals_sheet = os.environ["MEALS_SHEET"]
    # endregion
    g = os.environ["GOOGLE_CREDENTIALS"]
    print('f{g=}')
    # region get plan period
    plan_period = get_plan_period(DEFAULT_PLAN_PERIOD)

    # get meals list from meals list manager
    meals_list_manager = MealsListManager(
        google_cred_env=GOOGLE_ACCOUNT_CREDENTIALS_ENV_VAR,
        spreadsheet_name=SPREDSHEET_TITLE,
        worksheet_index=WORKSHEET_INDEX,
    )
    meals_list: list[MealItem] = meals_list_manager.get_meals_list()

    # generate meal plan
    meal_plan: list[MealItem] = meal_plan_generator.generate_meal_plan(
        meals_list, plan_period, datetime.date.today(), DAYS_MEAL_MUST_NOT_BE_SUGGESTED
    )
    # prepare mail notification data
    mail_subject: str = meal_plan_formatter.get_mail_subject(plan_period)
    mail_body: str = meal_plan_formatter.get_mail_body(
        meal_plan, plan_period, meals_sheet
    )
    # send notif mail with meal plan
    mailer = meal_planner.mail_notifier.MailNotifier(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        notification_mailbox=notification_mailbox,
        personal_mailbox=personal_mailbox,
        mail_password=mail_password,
    )
    mailer.send_notif_mail(mail_subject, mail_body)
    # update last suggested date for the meal
    meals_list_manager.update_meals_used_date(meals_list, meal_plan)


if __name__ == "__main__":
    main()
