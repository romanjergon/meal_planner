# meal_planner ![Tests](https://github.com/romanjergon/meal_planner/actions/workflows/tests.yml/badge.svg)

Have you ever had problem choosing a meal to cook for you and your family? Well, this planner solves this problem for
you. All you need is google sheet with your favorite meals and number of days cooked meal lasts for you.
Meal planner will choose meals for you to cook and send you mail with suggested meals to cook. 
## Features
 - prepares meal plan for your own list of favorite meals
 - sends meal plan by mail
 - notes last date each meal was suggested to
 - does not suggest the meal for next 14 days
 - choose time period for the meal plan from: TODAY, TOMORROW, NEXT_WEEK, NEXT_MONTH using command line args.

## Requirements
### Google sheet
Sheet must be in your Google Drive. Structure of sheet:

| Meal              | Note  | Days to serve             | Last s |   |
|-------------------|-------------------|------------------|--------|---|
| Lasagna bolognese | yummy             | 2             |        |   |
| Steak             | Buy meat at Aldi  | 1 |        |   |
| Veggie salad      |                   | 1                 |        |   |

### Add google service account
Follow the instructions for account at
https://owaisqureshi.medium.com/access-google-sheets-api-in-python-using-service-account-3a0c6d89d5fc
and download credential JSON.

### Mail 
Gmail is easiest to setup as its smtp server is setup in code. For gmail use app password see on how to set it up https://support.google.com/accounts/answer/185833?hl=en 
For other mail providers setup smtp and port in src/meal_planner/mail_notifier.py

### Setup .env for your passwords and mail addresses
Create standard .env file with following entries:

NOTIFICATION_MAILBOX=your.sender.address@gmail.com
MAIL_PASSWORD=mail_app_pass
PERSONAL_MAILBOX=your.recipient.address@anywhere.com
MEALS_SHEET=https://docs.google.com/spreadsheets/d/1MBCMhWn6MRtnY-4jYoJKlXNrUE0LPyyqcz96374uGqE/edit
GOOGLE_CREDENTIALS='String with contents of google service account credentials JSON'

To get string for GOOGLE_CREDENTIALS use python JSON.dumps with the contents of .JSON file as input.

### Localization for notification mail
Localization texts are in src/meal_planner/plan_period.py and src/meal_planner/meal_plan_formatter.py
Fork and change them to your language. When I see enough interest I will implement some localization support. 

### OPTIONAL Choose time period
Just run with argument --plan_period and value one of TODAY, TOMORROW, NEXT_WEEK, NEXT_MOTH.

## Tests and code quality
Just run everything via tox. To run tests use pytest.
Yes, tests do not cover everything, I am still on my path to TDD.