from django.shortcuts import render , redirect
from django.shortcuts import render ,redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import requests
from	django.utils.translation	import	gettext_lazy	as	_
from .forms import *
from .models import *





def notification_view(request,pk):
    if request.method == "GET" and request.user.is_superuser:
        notification = Notification.objects.get(pk=pk).notif
        return render(request,'notifications/notificationDetails.html',{'offer':notification})

    else:
        return redirect("home:posts")



@login_required
@require_POST
def message_view(request):
    if request.method == "POST" and request.is_ajax():
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        # End reCAPTCHA validation

        if result['success']:

            form = messageForm(request.POST)
            if form.is_valid():
                messageModel = form.save(commit = False)
                messageModel.user = User.objects.get(pk=request.user.pk)
                messageModel.save()

                message = _("thank you for your message , wait for our response.")
                data = {"message":message}
                print(data)
            else:
                message = _("your data is invalid ,please check it again.")
                data = {"errorMsg":message , "error":"1"}
                print(data)
        else:
            message = _("your data is invalid ,please check it and reCAPTCHA.")
            data = {"errorMsg":message , "error":"1"}
            print(data)
        return JsonResponse(data,status=200)


    else:
        message = _("Bad request , you can't access this page.")
        data = {"message":message}
        print(data)
        return JsonResponse(data,status=403)
