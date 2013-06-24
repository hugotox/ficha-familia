from datetime import date


def custom_context(request):
    this_year = date.today().year
    periods = range(2013, this_year + 1)
    return {
        'PERIODS': periods
    }
