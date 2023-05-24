from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class RqlPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    max_page_size = 1000  # Maximum number of items per page
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        start = (self.page.number - 1) * self.page.paginator.per_page + 1
        end = start + len(data) - 1

        return Response({
            'count': self.page.paginator.count,
            'start': start,
            'end': end,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
