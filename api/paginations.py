from rest_framework.pagination import PageNumberPagination


class JobPagination(PageNumberPagination):
    page_size = 10
    last_page_strings = ('last',)
    max_page_size = 12