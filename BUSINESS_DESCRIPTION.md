# Meal Planner Application - Business Description

This application automates weekly meal planning for a family. It performs the following tasks:

1. Reads a list of favorite meals from a Google Sheet stored on Google Drive.
2. Generates a meal plan for a predefined period (typically one week), ensuring variety and adherence to preferences.
3. Sends the generated meal plan via email to the designated recipient.

## Extended Functionality

- The application now plans both a main course and a soup for each day.
- The list of recipes in the Google Sheet must include a 'kind' column:
  - If 'kind' is 'soup', the meal is considered a soup.
  - All other values (including empty) are considered main courses.
- The application generates two separate plans (main courses and soups) and can present both in the meal plan email.
- The process is fully automated and scheduled to run every week using GitHub Actions, ensuring the family receives a fresh meal plan without manual effort.

## Key Features
- Prepares a meal plan from your own list of favorite meals (main courses and soups)
- Sends the meal plan by email
- Notes the last date each meal was suggested
- Does not suggest the same meal for the next 14 days
- Allows selection of the meal plan period: TODAY, TOMORROW, NEXT_WEEK, NEXT_MONTH
