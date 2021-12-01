from enum import Enum


class PlanPeriod(str, Enum):
    # since the most important recipient of meal plan is not proficient enough in English values are in Czech
    TODAY = "dnes"
    TOMORROW = "zítra"
    NEXT_WEEK = "příští týden"
    NEXT_MONTH = "příští měsíc"
