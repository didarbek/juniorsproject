from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination,)

class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 20


class PostPageNumberPagination(PageNumberPagination):
    page_size = 20
    