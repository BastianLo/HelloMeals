from rest_framework.pagination import PageNumberPagination

class RqlPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    max_page_size = 1000  # Maximum number of items per page
    page_size_query_param = 'page_size'