from django.shortcuts import render ,redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import requests
from	django.utils.translation	import	gettext_lazy	as	_
from .decorators import *
from .forms import *
# Create your views here.



#@ajax_required
@login_required
@require_POST
def offer_view(request,offer):

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
            form = offerForm(request.POST)
            if form.is_valid():
                offerModel = form.save(commit = False)
                offerModel.user = User.objects.get(pk=request.user.pk)
                offerModel.activitiy = offer
                offerModel.cost = offerModel.price * offerModel.amount
                offerModel.save()
                phone = offerModel.user.phone
                message = _("your request is completed successfully , you will get a call as soon as possible , in this phone number {}.".format(phone))
                data = {"message":message}
            else:
                message = _("your data is invalid ,please check it again.")
                data = {"errorMsg":message , "error":"1"}
        else:
            message = _("your data is invalid ,please check it and reCAPTCHA.")
            data = {"errorMsg":message , "error":"1"}
            print(data)
        return JsonResponse(data,status=200)


    else:
        #message = _("Bad request , you can't access this page.")
        #data = {"message":message}
        return redirect("home:posts")
