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
            #TODO: fix Weird workaround to remove = , which is added to drf filter - e.g. http://127.0.0.1:8000/api/Recipe?ilike(name,*hä*)=
            'next': self.get_next_link().replace("%29=", "%29") if self.get_next_link() is not None else None,
            'previous': self.get_previous_link().replace("%29=", "%29") if self.get_previous_link() is not None else None,
            'results': data
        })
