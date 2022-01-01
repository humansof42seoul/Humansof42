from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, reverse, redirect
from rest_framework.views import APIView
from .models import User,UserToken
from .ftauth import get_random_string, authenticate_ft_api
from django.conf import settings
from django.http import Http404


def log_in(request):
    if request.method == 'GET':
        ft_state = get_random_string(42)
        request.session['ft_state'] = ft_state
        ft_api_sign_in = "https://api.intra.42.fr/oauth/authorize"
        # redirect_uri = f"https://{request.get_host()}{reverse('ft_login')}"
        redirect_uri = f"http://{request.get_host()}{reverse('ft_login')}"
        response_type = "code"
        scope = "public"
        ft_sign_in_url = f"{ft_api_sign_in}?client_id={settings.FT_UID_KEY}&redirect_uri={redirect_uri}&response_type={response_type}&state={ft_state}&scope={scope}"
        return render(request, 'user/sign_in.html', {'ft_sign_in_url': ft_sign_in_url})


def ft_log_in(request):
    if request.method == 'GET':
        if request.session.get('ft_state') and request.session['ft_state'] != request.GET.get('state'):
            raise Http404("login error")
        ft_auth, ft_user_data = authenticate_ft_api(
            request.GET.get('code'),
            # f"https://{request.get_host()}{reverse('ft_login')}"
            f"http://{request.get_host()}{reverse('ft_login')}"
        )
        if ft_auth is None:
            raise Http404("invalid user")
        request.session['login_user'] = ft_user_data["login"] #login==intra id
        user = authenticate(login=ft_user_data["login"])
        if user:
            login(request, user)
            if user.is_staff:
                request.session['is_admin'] = True
            return redirect('main')
        else:
            user = User.objects.create_user(
                id = ft_user_data["id"],
                email = ft_user_data["email"],
                login = ft_user_data["login"],
            )
            usertoken = UserToken.objects.create(user=user, ft_token=ft_auth.get_refresh_token())
            usertoken.save()
            # user.usertoken.ft_token = ft_auth.get_refresh_token()
            # user.usertoken.save()
            login(request, user)

        if next_url := request.GET.get('next'):
            return redirect(next_url)
        else:
            return redirect('main')


def log_out(request):
    if request.method == "GET":
        return render(request, 'user/ft_sign_out.html')
    if request.method == "POST":
        logout(request)
        return redirect('main')