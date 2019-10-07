from django.shortcuts import render , redirect

from django.utils.safestring import mark_safe
import json
from django.views.generic import View
from accounts.models import User


class Index(View):  # render the home page.
    def get(self, request):
        try:
            user = User.objects.get(username = request.user.username)
            if user and user.is_authenticated:
                if user.profile.profileComplete:
                    return render(request, 'home/home.html')
                else:
                    return redirect("profiles:password_set",request.user.username)
            else:
                return render(request, 'home/home.html')
        except:
            return render(request, 'home/home.html')
