from django.contrib import admin
from mptt.admin import MPTTModelAdmin


from .models import Node

admin.site.register(Node, MPTTModelAdmin)