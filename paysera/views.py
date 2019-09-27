from django.shortcuts import render , redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import *
from offers.models import *
from notifications.models import *
# Create your views here.



def dash_board_view(request):
    offers = Notification.objects.filter(msg=None).count()
    messages = Notification.objects.filter(notif=None).count()
    if offers > 0 :
        offers = Notification.objects.filter(msg=None).order_by('-date')
    else:
        offers = None
    if messages > 0 :
        messages = Notification.objects.filter(notif=None).order_by('-date')
    else:
        messages = None

    return render(request,"paysera/dash_board.html",{"offers" : offers , "messages" : messages })

@login_required
@require_POST
def dash_board_ajax(request,notification,action,pk):
    if request.method == "POST" and request.is_ajax() and request.user.is_superuser:
        if action == "remove":
            if notification == "offer":
                Offer.objects.get(pk = pk).delete()
            else:
                Message.objects.get(pk = pk).delete()
        elif action == "check":
            if notification == "offer":
                offer = Offer.objects.get(pk = pk)
                offer.notification.seen = True
                offer.save()
            else:
                message = Message.objects.get(pk = pk)
                message.notification.seen = True
                message.save()
        else:
            if notification == "offer":
                offer = Offer.objects.get(pk = pk)
                offer.notification.seen = False
                offer.save()
            else:
                message = Message.objects.get(pk = pk)
                message.notification.seen = False
                message.save()
        return JsonResponse({ "data":"operation done"},status=200)
    else:
        return redirect("home:posts")
