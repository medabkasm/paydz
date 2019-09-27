from django.shortcuts import render

from django.utils.safestring import mark_safe
import json
from django.views.generic import View



class Index(View):  # render the home page.
    def get(self, request):
        return render(request, 'home/home.html')

def index(request):
    return render(request, 'home/index.html', {})

def room(request, room_name):
    return render(request, 'home/room.html', {'room_name_json': mark_safe(json.dumps(room_name))})
