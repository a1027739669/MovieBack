from .models import *
from django.contrib import admin
from django.core.paginator import Paginator, cached_property
from django.db import connections
class LargeTablePaginator(Paginator):
    def _get_count(self):
        return 1400000
    count = property(_get_count)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userid','username')
    show_full_result_count = False
    paginator = LargeTablePaginator

