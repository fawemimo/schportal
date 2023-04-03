from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    page_size = 1
    last_page_strings = ("last",)
    max_page_size = 1
