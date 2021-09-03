from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """
    Limit results prt page (/?limit=)
    If hasn't query_param will be 10 items on page by default
    """

    page_size = 10
    page_query_param = "page"
    page_size_query_param = "limit"
