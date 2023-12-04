from django.contrib import admin

from .models import Vendor
from .models import Record

admin.site.register(Vendor)
admin.site.register(Record)
