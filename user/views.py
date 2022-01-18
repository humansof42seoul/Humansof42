from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, reverse, redirect
from .models import User,UserToken
from .forms import EmailChangeForm, LoginForm
from .ftauth import get_random_string, authenticate_ft_api
from django.conf import settings
from django.http import Http404

@login_required
def change_email(request):
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, request.user)
        if form.is_valid():
            email = request.POST.get('email')
            user = request.user
            user.email = email
            user.save()
            messages.success(request, 'Your email was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    return render(request, 'user/mypage.html', {'email_form': form, 'password_form': password_form})

@login_required
def change_password(request):
    email_form = EmailChangeForm(instance=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    return render(request, 'user/mypage.html', {'email_form': email_form, 'password_form': form})

def log_in(request):
    form = LoginForm()
    ft_state = get_random_string(42)
    request.session['ft_state'] = ft_state
    ft_api_sign_in = "https://api.intra.42.fr/oauth/authorize"
    redirect_uri = f"https://{request.get_host()}{reverse('ft_login')}"
    response_type = "code"
    scope = "public"
    ft_sign_in_url = f"{ft_api_sign_in}?client_id={settings.FT_UID_KEY}&redirect_uri={redirect_uri}&response_type={response_type}&state={ft_state}&scope={scope}"
    if request.method == 'GET':
        return render(request, 'user/sign_in.html', {'ft_sign_in_url': ft_sign_in_url})
    elif request.method == 'POST':
        form = LoginForm(request.POST, request.user)
        email = request.POST['email']
        password = request.POST['password']
        user = find_user_with_email(email)
        user = authenticate(login = user.login, password = password)
        if user:
            login(request, user)
            return redirect('main')
    return render(request, 'user/sign_in.html', {'ft_sign_in_url': ft_sign_in_url, 'form': form})


def ft_log_in(request):
    if request.method == 'GET':
        if request.session.get('ft_state') and request.session['ft_state'] != request.GET.get('state'):
            raise Http404("login error")
        ft_auth, ft_user_data = authenticate_ft_api(
            request.GET.get('code'),
            f"https://{request.get_host()}{reverse('ft_login')}"
            # f"http://{request.get_host()}{reverse('ft_login')}"
        )
        if ft_auth is None:
            raise Http404("invalid user")
        request.session['login_user'] = ft_user_data["login"] #login==intra id
        user = find_user_with_id(ft_user_data["id"])
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

def find_user_with_id(id):
    user = User.objects.filter(id=id).first()
    return user

def find_user_with_email(email):
    user = User.objects.filter(email=email).first()
    return user

def log_out(request):
    if request.method == "GET":
        return render(request, 'user/ft_sign_out.html')
    if request.method == "POST":
        logout(request)
        return redirect('main')

def get_mypage(request):
    email_form = EmailChangeForm(instance = request.user)
    password_form = PasswordChangeForm(request.user)
    return render(request, 'user/mypage.html', {'email_form': email_form, 'password_form': password_form})
