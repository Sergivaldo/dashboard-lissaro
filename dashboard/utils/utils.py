import locale


def format_value( value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    value = locale.currency(value, grouping=True, symbol=None)

    return value
