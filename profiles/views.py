from django.shortcuts import render , redirect
from notifications.models import *
from accounts.models import *
from django.core import serializers
import json
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from	django.utils.translation	import	gettext_lazy	as	_
from django.contrib import messages
from django.contrib.auth import logout
from .forms import *
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from accounts.models import *


@login_required
def profile_view(request,username):

    if request.user.username == username:
        user = User.objects.get(username = username)
        profile = Profile.objects.get(user = user)
        profileForm = profileEditForm(instance = user)
        userForm = userEditForm(instance = profile)
        return render(request,'profiles/profile.html',
                    {
                         'userForm': userForm,
                         'profileForm': profileEditForm,
                    })
    else:
       return redirect("home:posts")



@login_required
@require_POST
def profile_edit_view_ajax(request,username):
    if request.method == "POST" and request.is_ajax() and request.user.username == username :
        user = request.user
        profile = Profile.objects.get(user = user)
        profileEdit = profileEditForm(instance = profile , data = request.POST)

        if profileEdit.is_valid():
            print(profile)
            profileEdit.save()
            profileJson = serializers.serialize('json',[user.profile,])  # json data with wrapper with [].
            profile = json.loads(profileJson)
            return JsonResponse({"profile" : profile[0]['fields']},status = 200)
        else:
            print(profileEdit.errors)
            return JsonResponse({"data":profileEdit.errors},status = 500)
    else:
        return redirect("home:posts")




@login_required
@require_POST
def profile_delete_view_ajax(request,username):
    if request.method == "POST" and request.is_ajax():
        if request.user.username == username:
            User.objects.get(username = username).delete()
            message = _("Your Account was deleted successfully.")
            messages.info(request,message)
            return JsonResponse({"data":"success"},status = 200)
        else:
            return redirect("home:posts")
    else:
        return redirect("home:posts")



@login_required
@require_POST
def profile_view_ajax(request,username,data):

    if request.method == "POST" and request.is_ajax():

        if data == "offer" and Notification.objects.filter(msg=None).count() > 0 :
            notifications = Notification.objects.filter(msg=None).order_by('-date')
            dataList = []
            for notification in notifications:
                notif = serializers.serialize('json',[notification.notif,])  # json data with wrapper with [].
                item = json.loads(notif)  # get ride of [].
                dataList.append(item[0]['fields'])
            jsonData = {
                    "dataList": dataList,
                    "count": len(dataList)
                    }

        elif data == "message" and Notification.objects.filter(notif=None).count() > 0 :
            notifications = Notification.objects.filter(notif=None).order_by('-date')
            dataList = []
            dataDict = {}
            for notification in notifications:
                notif = serializers.serialize('json',[notification.msg,])  # json data with wrapper with [].
                item = json.loads(notif)  # get ride of [].
                dataList.append(item[0]['fields'])

            jsonData = {
                    "dataList": dataList,
                    "count": len(dataList)
                }

        else:
            empty = _("No data found.")
            return JsonResponse({"count":0 , "dataList":empty},status = 200)

        return JsonResponse(jsonData,status=200)

    else:
        return redirect("home:posts")




@login_required
def password_set_view(request,username):
    if request.user.username == username:
        if request.user.has_usable_password():
            return redirect('profiles:password_change',request.user.username)
        else:
            PasswordForm = AdminPasswordChangeForm

        if request.method == 'POST':
            form = PasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                message = _("Your password was successfully seted!")
                user = User.objects.get(username = username)
                user.profile.profileComplete = True
                user.save()
                messages.info(request,message)
                return redirect('home:posts')
            else:
                return render(request, 'profiles/password_set.html', {'form': form})
        else:
            form = PasswordForm(request.user)
        return render(request, 'profiles/password_set.html', {'form': form})
    else:
        return redirect('profiles:password_set',request.user.username)
