from meal_planner.mealitem import MealItem
from meal_planner.plan_period import PlanPeriod


def get_mail_subject(plan_period: PlanPeriod) -> str:
    return f"Návrh plánu na vaření na {plan_period.value}"


def get_mail_body(
    meal_plan: list[MealItem], plan_period: PlanPeriod, meals_sheet: str
) -> str:
    GOOGLE_SEARCH_ENDPOINT = "https://www.google.com/search?q="

    # Czech description, change according to your liking
    mail_body: str = (
        f"Toto je romanovým automatem navržený plán obědů na období {plan_period.value} "
        f"vygenerovaný dle seznamu oblíbených jídel {meals_sheet} . \n"
        f"Můžeš jej klidně ignorovat, ale vždycky je tak těžké něco vybrat. "
        f"A tak jsem si řekl, že by ti toto mohlo pomoci.\n "
        f"Čím více jídel bude v seznamu oblíbených, tím lepší tento vyběr bude. "
        f"Čím lepší název jídel bude, tím lepší budou odkazy na google. Jen prosím nemeň popisky v záhlaví.\n\n"
    )
    for meal in meal_plan:
        mail_body += (
            f"Den: {meal.last_suggested}, {meal.name}, mělo by vystačit na {meal.days_to_serve} dny, "
            f"recepty dle google: {GOOGLE_SEARCH_ENDPOINT}{meal.name.replace(' ','+')} \n"
        )
    if len(meal_plan) == 0:
        mail_body += (
            "Z nějakého důvodu se nezdařilo vygenerovat plán jídel, "
            "zřejmě nejsou na výběr žádná jídla "
            "anebo nejsou na výběr žádná jídla, která by nebyla nedávno doporučená."
        )
    return mail_body
