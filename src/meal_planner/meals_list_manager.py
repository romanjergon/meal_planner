import datetime
import os

import pygsheets

from meal_planner.mealitem import MealItem


class MealsListManager:
    def __init__(
        self, google_cred_env: str, spreadsheet_name: str, worksheet_index: int
    ):

        # hack for escape chars in GitHub action
        g = os.environ[google_cred_env].replace('\\\\n', '\\n')
        with open('./google_creds.json', 'w') as cred_file:
            cred_file.write(g)

        self.gsheet_client: pygsheets.client = pygsheets.authorize(service_file='./google_creds.json'
        )
        # hack for escape chars in GitHub action cleaning up
        os.remove('./google_creds.json')

        # self.gsheet_client: pygsheets.client = pygsheets.authorize(
        #     service_account_env_var=google_cred_env
        # )
        self.spreadsheet_name: str = spreadsheet_name
        self.worksheet_index: int = worksheet_index

    def get_meals_sheet_pygsheets(self) -> pygsheets.worksheet:
        meals_spreadsheet: pygsheets.spreadsheet = self.gsheet_client.open(
            self.spreadsheet_name
        )
        current_worksheet: pygsheets.worksheet = meals_spreadsheet.worksheet(
            value=self.worksheet_index
        )
        return current_worksheet

    def get_meals_list(
        self,
    ) -> list[MealItem]:
        sheet: pygsheets.worksheet = self.get_meals_sheet_pygsheets()
        # dictionary with values str, int, date
        all_records: list[dict[str, any]] = sheet.get_all_records()  # type: ignore[valid-type]
        for record in all_records:
            if record["Last suggested to"] == "":
                record["Last suggested to"] = None
            else:
                record["Last suggested to"] = datetime.date.fromisoformat(
                    record["Last suggested to"]
                )

        meals_list: list[MealItem] = [
            MealItem(meal["Meal"], meal["Days to serve"], meal["Last suggested to"])
            for meal in all_records
        ]
        return meals_list

    def update_meals_used_date(
        self, meals_list: list[MealItem], meal_plan: list[MealItem]
    ) -> None:
        # copy last day suggested from plan
        for meal in meal_plan:
            m = next(filter(lambda x: x.name == meal.name, meals_list))
            m.last_suggested = meal.last_suggested

        # save the date to google sheet
        sheet: pygsheets.worksheet = self.get_meals_sheet_pygsheets()

        last_suggested_dates: list[str] = []
        for meal in meals_list:
            if meal.last_suggested is None:
                last_suggested_dates.append("")
            else:
                last_suggested_dates.append(str(meal.last_suggested))

        sheet.update_col(index=4, values=last_suggested_dates, row_offset=1)
