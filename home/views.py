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
from django.contrib.auth.decorators import login_required

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

# def callback(request):
#     token = oauth.auth0.authorize_access_token(request)
#     request.session["user"] = token
#     return redirect(request.build_absolute_uri(reverse("home")))

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

@login_required
def logout(request):
    django_logout(request)
    domain = settings.AUTH0_DOMAIN
    client_id = settings.AUTH0_CLIENT_ID
    return_to = 'http://127.0.0.1:8000' # this can be current domain
    return redirect(f"https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}")


@login_required
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



