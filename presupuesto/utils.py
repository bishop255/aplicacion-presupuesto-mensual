from datetime import date


MONTH_NAMES = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]

SHORT_MONTH_NAMES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


def money(value):
    try:
        return f"$ {int(round(float(value))):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "$ 0"


def parse_money(value):
    cleaned = str(value).replace("$", "").replace(".", "").replace(",", "").strip()
    if not cleaned:
        return 0
    return int(float(cleaned))


def month_key(day=None):
    day = day or date.today()
    return f"{day.year:04d}-{day.month:02d}"


def month_label(key):
    year, month = map(int, key.split("-"))
    return f"{MONTH_NAMES[month - 1]} {year}"


def short_month_label(month):
    return SHORT_MONTH_NAMES[month - 1]

