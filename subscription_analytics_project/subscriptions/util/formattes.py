

import locale

def format_currency(value):
    """
    Formata o valor para moeda BRL (Real Brasileiro).
    """
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Define a localidade para o Brasil
    return locale.currency(value, grouping=True)

def format_mrr(mrr):
    """
    Formata o Monthly Recurring Revenue (MRR) para moeda BRL (Real Brasileiro).
    """
    return format_currency(mrr)


def format_churn(churn):
    """
    Formata o Churn Rate para duas casas.
    """
    return '{:.2f}'.format(churn)

