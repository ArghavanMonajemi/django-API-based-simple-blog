from rest_framework.pagination import CursorPagination

class StandardCursorPagination(CursorPagination):
    page_size = 3
    ordering = '-pub_date'