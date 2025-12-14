# Meal Planner Application

> **Important:** If you get `ModuleNotFoundError: No module named 'meal_planner'`, set the PYTHONPATH to `src` before running the application. On Windows PowerShell, use:
>
>     $env:PYTHONPATH="src"; poetry run python -m meal_planner.main
>
> This ensures Python can find the `meal_planner` package inside the `src` directory.

> **For a detailed business description of this application, see [BUSINESS_DESCRIPTION.md](./BUSINESS_DESCRIPTION.md).**

# How to Run the Meal Planner Application

## Prerequisites

- Python 3.8 or newer (see `pyproject.toml` for exact version)
- [Poetry](https://python-poetry.org/) for dependency management
- Google service account credentials (for Google Sheets access)
- Gmail or SMTP credentials for sending emails

## Setup

1. **Clone the repository**

2. **Install Poetry** (if not already installed):
   ```
   pip install poetry
   ```

3. **Install dependencies using Poetry**
   ```
   poetry install
   ```

4. **Create a `.env` file in the project root** with the following entries:
   ```
   NOTIFICATION_MAILBOX=your.sender.address@gmail.com
   MAIL_PASSWORD=mail_app_pass
   PERSONAL_MAILBOX=your.recipient.address@anywhere.com
   MEALS_SHEET=https://docs.google.com/spreadsheets/your-sheet-id/edit
   GOOGLE_CREDENTIALS='String with contents of google service account credentials JSON'
   ```
   - For `GOOGLE_CREDENTIALS`, use Python's `json.dumps` to convert your credentials JSON file to a string.

5. **Prepare your Google Sheet**
   - The sheet must be in your Google Drive and follow this structure:
     | Meal              | Note              | Days to serve | Last s |   |
     |-------------------|-------------------|---------------|--------|---|
     | Lasagna bolognese | yummy             | 2             |        |   |
     | Steak             | Buy meat at Aldi  | 1             |        |   |
     | Veggie salad      |                   | 1             |        |   |

6. **(Optional) Edit localization**
   - To change notification mail language, edit `src/meal_planner/plan_period.py` and `src/meal_planner/meal_plan_formatter.py`.

## Running the Application

To generate and send a meal plan, run:
```
poetry run python -m meal_planner.main
```

- By default, the plan is for the next week.
- To specify a different period, use:
  ```
  poetry run python -m meal_planner.main --plan_period TODAY
  ```
  Valid values: `TODAY`, `TOMORROW`, `NEXT_WEEK`, `NEXT_MONTH`

## Automated Weekly Run

- The application is set up to run weekly via GitHub Actions. No manual intervention is needed for scheduled runs.

## Testing

- To run tests:
  ```
  poetry run tox
  ```
  or
  ```
  poetry run pytest
  ```
