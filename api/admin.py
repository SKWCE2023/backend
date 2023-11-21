from django.contrib import admin
from .models import *

admin.site.register(Service)
admin.site.register(Users)
admin.site.register(Customers)
admin.site.register(Order)
admin.site.register(ServiceRendered)
admin.site.register(LoginHistory)
admin.site.register(UtilizerOperation)