from django.contrib import admin

from web.admin.staff import StaffAdmin
from web.models import Staff

admin.site.register(Staff, StaffAdmin)
