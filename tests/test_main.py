import datetime
from unittest import mock

import pytest

from meal_planner.main import get_plan_period, main
from meal_planner.plan_period import PlanPeriod


class TestGetPlanPeriod:
    """Tests for CLI argument parsing function."""

    def test_get_plan_period_default(self):
        """Should return default period when no arguments provided."""
        with mock.patch("sys.argv", ["main.py"]):
            result = get_plan_period(PlanPeriod.NEXT_WEEK)
            assert result == PlanPeriod.NEXT_WEEK

    def test_get_plan_period_today(self):
        """Should parse TODAY argument correctly."""
        with mock.patch("sys.argv", ["main.py", "--plan_period", "TODAY"]):
            result = get_plan_period(PlanPeriod.NEXT_WEEK)
            assert result == PlanPeriod.TODAY

    def test_get_plan_period_tomorrow(self):
        """Should parse TOMORROW argument correctly."""
        with mock.patch("sys.argv", ["main.py", "--plan_period", "TOMORROW"]):
            result = get_plan_period(PlanPeriod.NEXT_WEEK)
            assert result == PlanPeriod.TOMORROW

    def test_get_plan_period_next_week(self):
        """Should parse NEXT_WEEK argument correctly."""
        with mock.patch("sys.argv", ["main.py", "--plan_period", "NEXT_WEEK"]):
            result = get_plan_period(PlanPeriod.TODAY)
            assert result == PlanPeriod.NEXT_WEEK

    def test_get_plan_period_next_month(self):
        """Should parse NEXT_MONTH argument correctly."""
        with mock.patch("sys.argv", ["main.py", "--plan_period", "NEXT_MONTH"]):
            result = get_plan_period(PlanPeriod.NEXT_WEEK)
            assert result == PlanPeriod.NEXT_MONTH

    def test_get_plan_period_short_flag(self):
        """Should handle short -p flag."""
        with mock.patch("sys.argv", ["main.py", "-p", "TODAY"]):
            result = get_plan_period(PlanPeriod.NEXT_WEEK)
            assert result == PlanPeriod.TODAY

    def test_get_plan_period_invalid_value(self):
        """Should raise ValueError for invalid plan period."""
        with mock.patch("sys.argv", ["main.py", "--plan_period", "INVALID"]):
            with pytest.raises(ValueError, match="Wrong plan_period value"):
                get_plan_period(PlanPeriod.NEXT_WEEK)

    def test_get_plan_period_case_sensitive(self):
        """Should be case-sensitive and reject lowercase values."""
        with mock.patch("sys.argv", ["main.py", "--plan_period", "today"]):
            with pytest.raises(ValueError, match="Wrong plan_period value"):
                get_plan_period(PlanPeriod.NEXT_WEEK)


class TestMainIntegration:
    """Integration tests for the main() function."""

    @mock.patch("meal_planner.main.MealsListManager")
    @mock.patch("meal_planner.main.mail_notifier.MailNotifier")
    @mock.patch("meal_planner.main.meal_plan_generator.generate_meal_plan")
    @mock.patch("meal_planner.main.meal_plan_formatter.get_mail_subject")
    @mock.patch("meal_planner.main.meal_plan_formatter.get_mail_body")
    @mock.patch("meal_planner.main.get_plan_period")
    @mock.patch.dict(
        "os.environ",
        {
            "NOTIFICATION_MAILBOX": "test@test.com",
            "MAIL_PASSWORD": "password",
            "PERSONAL_MAILBOX": "personal@test.com",
            "MEALS_SHEET": "https://docs.google.com/spreadsheets/test",
            "GOOGLE_CREDENTIALS": "test_credentials",
        },
    )
    def test_main_executes_successfully(
        self,
        mock_get_plan_period,
        mock_get_mail_body,
        mock_get_mail_subject,
        mock_generate_meal_plan,
        mock_mail_notifier,
        mock_meals_list_manager,
    ):
        """Should execute main workflow without errors."""
        from meal_planner.mealitem import MealItem

        # Setup mocks
        mock_get_plan_period.return_value = PlanPeriod.NEXT_WEEK

        # Mock meals list
        test_meals = [
            MealItem("Steak", 2, "dinner", None),
            MealItem("Soup", 1, "soup", None),
        ]
        mock_manager_instance = mock_meals_list_manager.return_value
        mock_manager_instance.get_meals_list.return_value = test_meals

        # Mock meal plan generation
        mock_generate_meal_plan.side_effect = [
            [MealItem("Steak", 2, "dinner", datetime.date(2025, 12, 22))],
            [MealItem("Soup", 1, "soup", datetime.date(2025, 12, 22))],
        ]

        # Mock formatter
        mock_get_mail_subject.return_value = "Test Subject"
        mock_get_mail_body.return_value = "Test Body"

        # Mock mail notifier
        mock_notifier_instance = mock_mail_notifier.return_value
        mock_notifier_instance.send_notif_mail.return_value = {}

        # Execute main
        main()

        # Verify workflow
        mock_get_plan_period.assert_called_once_with(PlanPeriod.NEXT_WEEK)
        mock_manager_instance.get_meals_list.assert_called_once()
        assert (
            mock_generate_meal_plan.call_count == 2
        )  # Once for main courses, once for soups
        mock_get_mail_subject.assert_called_once_with(PlanPeriod.NEXT_WEEK)
        mock_get_mail_body.assert_called_once()
        mock_notifier_instance.send_notif_mail.assert_called_once_with(
            "Test Subject", "Test Body"
        )
        mock_manager_instance.update_meals_used_date.assert_called_once()

    @mock.patch("meal_planner.main.MealsListManager")
    @mock.patch("meal_planner.main.mail_notifier.MailNotifier")
    @mock.patch("meal_planner.main.meal_plan_generator.generate_meal_plan")
    @mock.patch("meal_planner.main.meal_plan_formatter.get_mail_subject")
    @mock.patch("meal_planner.main.meal_plan_formatter.get_mail_body")
    @mock.patch("meal_planner.main.get_plan_period")
    @mock.patch.dict(
        "os.environ",
        {
            "NOTIFICATION_MAILBOX": "test@test.com",
            "MAIL_PASSWORD": "password",
            "PERSONAL_MAILBOX": "personal@test.com",
            "MEALS_SHEET": "https://docs.google.com/spreadsheets/test",
            "GOOGLE_CREDENTIALS": "test_credentials",
        },
    )
    def test_main_separates_soups_and_main_courses(
        self,
        mock_get_plan_period,
        mock_get_mail_body,
        mock_get_mail_subject,
        mock_generate_meal_plan,
        mock_mail_notifier,
        mock_meals_list_manager,
    ):
        """Should separate soups from main courses correctly."""
        from meal_planner.mealitem import MealItem

        # Setup mocks
        mock_get_plan_period.return_value = PlanPeriod.NEXT_WEEK

        # Mock meals list with various kinds
        test_meals = [
            MealItem("Steak", 2, "dinner", None),
            MealItem("Chicken Soup", 1, "soup", None),
            MealItem("Tomato Soup", 1, "SOUP", None),  # uppercase
            MealItem("Goulash Soup", 1, " soup ", None),  # with spaces
            MealItem("Pizza", 2, "lunch", None),
            MealItem("Pasta", 2, None, None),  # None kind
            MealItem("Salad", 1, "", None),  # empty kind
        ]
        mock_manager_instance = mock_meals_list_manager.return_value
        mock_manager_instance.get_meals_list.return_value = test_meals

        # Mock meal plan generation
        mock_generate_meal_plan.side_effect = [
            [MealItem("Steak", 2, "dinner", datetime.date(2025, 12, 22))],
            [MealItem("Chicken Soup", 1, "soup", datetime.date(2025, 12, 22))],
        ]

        # Mock formatter and notifier
        mock_get_mail_subject.return_value = "Test"
        mock_get_mail_body.return_value = "Test"
        mock_notifier_instance = mock_mail_notifier.return_value
        mock_notifier_instance.send_notif_mail.return_value = {}

        # Execute main
        main()

        # Verify generate_meal_plan was called twice with correct meal lists
        assert mock_generate_meal_plan.call_count == 2

        # First call should have main courses (non-soup items)
        main_courses_call = mock_generate_meal_plan.call_args_list[0]
        main_courses_list = main_courses_call[0][0]
        main_course_names = [m.name for m in main_courses_list]
        assert "Steak" in main_course_names
        assert "Pizza" in main_course_names
        assert "Pasta" in main_course_names
        assert "Salad" in main_course_names
        assert "Chicken Soup" not in main_course_names
        assert "Tomato Soup" not in main_course_names
        assert "Goulash Soup" not in main_course_names

        # Second call should have soups
        soups_call = mock_generate_meal_plan.call_args_list[1]
        soups_list = soups_call[0][0]
        soup_names = [m.name for m in soups_list]
        assert "Chicken Soup" in soup_names
        assert "Tomato Soup" in soup_names
        assert "Goulash Soup" in soup_names
        assert len(soups_list) == 3

    @mock.patch.dict(
        "os.environ",
        {},  # Empty environment
        clear=True,
    )
    def test_main_raises_error_when_env_vars_missing(self):
        """Should raise KeyError when required environment variables are missing."""
        with pytest.raises(KeyError):
            main()
