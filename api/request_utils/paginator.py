from django.core.paginator import Paginator


def paginate(record, skip):
    paginator = Paginator(record, 15)
    page_number = skip or 1
    return paginator.page(page_number)
