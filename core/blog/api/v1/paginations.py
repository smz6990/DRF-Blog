from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class
    """

    page_size = 4

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total posts": self.page.paginator.count,
                "total pages": self.page.paginator.num_pages,
                "current page": self.page.number,
                "no. of posts in this page": len(data),
                "results": data,
            }
        )
