from rest_framework.pagination import CursorPagination
from rest_framework.pagination import PageNumberPagination


class MyCursorPagination(CursorPagination):
    page_size = 1
    ordering = ['name']


class MyPageNumberPagination(PageNumberPagination):
    page_size = 2
