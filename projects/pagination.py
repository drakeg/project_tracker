"""Pagination classes for the project tracker API."""

from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class StandardPageNumberPagination(PageNumberPagination):
    """Page-number pagination with a bounded client-selectable page size."""

    page_size_query_param = "page_size"
    max_page_size = settings.API_MAX_PAGE_SIZE
