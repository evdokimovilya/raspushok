from django.shortcuts import render
from django.http import HttpResponse

from .models import Node

def main(request):

    nodes = Node.objects.filter()

    return render(request, 'main.html', {'nodes': nodes})
