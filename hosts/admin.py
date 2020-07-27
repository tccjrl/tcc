from django.contrib import admin
from .models import Host, Item, Template

admin.site.register(Host)
admin.site.register(Item)
admin.site.register(Template)
