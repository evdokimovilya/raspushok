
from django.contrib import admin
from django.urls import path

from . import views 

urlpatterns = [
    path('', views.main),
    path('nodes/<int:node_id>', views.add_node, name='add_node')
]
