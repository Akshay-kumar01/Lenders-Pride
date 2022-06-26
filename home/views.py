import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from decouple import config


# Create your views here.
def home(request):
     return render(
        request,
        "home.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )

def about(request):
    return render(request, "about.html");


def logout(request):
    django_logout(request)

    domain=config('APP_DOMAIN')
    client_id=config('APP_CLIENT_ID')
    return_to='http://127.0.0.1:8000/'

    return HttpResponseRedirect(f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}")


def profile(request):
    user=request.user

    auth0_user=user.social_auth.get(provider='auth0')

    user_data={
        'user_id':auth0_user.uid,
        'name':user.first_name,
        'picture':auth0_user.extra_data['picture']
    }

    context={
        'user_data':json.dumps(user_data,indent=4),
        'auth0_user':auth0_user
    }


    return render(request,'profile.html',context)



