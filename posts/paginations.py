from rest_framework.pagination import LimitOffsetPagination

class Paginatin(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10