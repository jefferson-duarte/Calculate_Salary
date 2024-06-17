def price_format(price):
    return f'€ {price:.2f}'.replace('.', ',')


def one_float(value):
    return f'{value:.0f}'
