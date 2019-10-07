from django.shortcuts import render , redirect
from django.template.loader import render_to_string
from django.views.generic import View
from .models import User,Profile
from home.models import Post
from .forms import *  # RegisterForm
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from	django.utils.translation	import	gettext_lazy	as	_
import requests
from django.conf import settings
from .decorators import check_recaptcha
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

class ProfileView(View):  # user profile reachable from  /profile/username URL , username is unique for each user.
    def get(self,request,username):
        parms = {}
        user = User.objects.get(username = username)   # get the user obj with the username.
        posts = Post.objects.filter(user = user)  # get all posts of the user , with the username = username.
        parms["posts"] = posts
        parms["user"] = user

        return render(request, 'accounts/profile.html', parms)



# may way to handle form rendering.
class	RegisterView(View):
    def post(self,request):
        form = RegisterForm(request.POST)
        #profileForm = profileEditForm(request.POST,request.FILES)
        agree = request.POST.get('agree-term')

        if	form.is_valid()  and agree:

            # rechaptcha validation
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            # End reCAPTCHA validation

            if result['success']:
                #	Create	a	new	user	object	but	avoid	saving	it	yet
                new_user = form.save(commit=False)
                #	Set	the	chosen	password
                new_user.set_password(form.cleaned_data['password1'])
                #new_profile = profileForm.save()
                #new_user.profile = new_profile
                #	Save	the	User	object
                new_user.is_active = False
                new_user.save()
                current_site = get_current_site(request)
                email_subject = _('Activate Your Account')
                message = render_to_string('accounts/registration/activate_account.html', {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': account_activation_token.make_token(new_user),
                    })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(email_subject, message, to=[to_email])
                email.send()

                message = _("Your account has been successfully created ,we sent you an email message with   confirmation link, Please check your email and follow the link ,to make activate your PayDz account .")
                messages.info(request,message)
                return render(request,'accounts/register.html',{'form':form})
            else:
                agreeErrorText = _("you must agree to all statements in Terms of service")
                recaptchaErrorText = _("Invalid reCAPTCHA. Please try again.")
                return render(request,'accounts/register.html',{'form':form,'recaptcha':recaptchaErrorText})

        else:
            agreeErrorText = _("you must agree to all statements in Terms of service")
            recaptchaErrorText = _("Invalid reCAPTCHA. Please try again.")
            return render(request,'accounts/register.html',{'form':form,'agreeError':agreeErrorText,'recaptcha':recaptchaErrorText})

    def get(self,request):
        if request.user.is_authenticated:
            return	render(request,'accounts/home.html')

        form = RegisterForm()
        return render(request,'accounts/register.html',{'form':form})


# may way to handle form rendering.
def	RegisterView_ajax(request):
    if request.method == "POST" and request.is_ajax():
        form = RegisterForm(request.POST)
        #profileForm = profileEditForm(request.POST,request.FILES)
        agree = request.POST.get('agree-term')

        if	form.is_valid()  and agree:
            # rechaptcha validation
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            # End reCAPTCHA validation

            if result['success']:
                #	Create	a	new	user	object	but	avoid	saving	it	yet
                new_user = form.save(commit=False)
                #	Set	the	chosen	password
                new_user.set_password(form.cleaned_data['password1'])
                #new_profile = profileForm.save()
                #new_user.profile = new_profile
                #	Save	the	User	object
                new_user.is_active = False
                new_user.save()
                current_site = get_current_site(request)
                email_subject = _('Activate Your Account')
                message = render_to_string('accounts/registration/activate_account.html', {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': account_activation_token.make_token(new_user),
                    })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(email_subject, message, to=[to_email])
                email.send()

                message = _("Your account has been successfully created ,we sent you an email message with   confirmation link, Please check your email and follow the link ,to make activate your PayDz account .")

                return JsonResponse({"message":message},status =200 )
            else:
                agreeErrorText = _("you must agree to all statements in Terms of service")
                recaptchaErrorText = _("Invalid reCAPTCHA. Please try again.")
                return JsonResponse({"message":"error"} ,status = 400)
        else:
            agreeErrorText = _("you must agree to all statements in Terms of service")
            recaptchaErrorText = _("Invalid reCAPTCHA. Please try again.")
            return JsonResponse(form.errors ,status = 400)


    elif request.method == "GET":
        if request.user.is_authenticated:
            return	render(request,'accounts/home.html')

        form = RegisterForm()
        return render(request,'accounts/register.html',{'form':form})




def user_activation_view(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        text = _('Activation link is invalid!')
        messages.error(request,text)
        return redirect('accounts:register')

    if user  and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.profileComplete = True
        user.save()
        text = _('Your account has been activated successfully')
        messages.info(request,text)
        return redirect('accounts:login')
    else:
        text = _('Activation link is invalid!')
        messages.error(request,text)
        return redirect('accounts:register')
