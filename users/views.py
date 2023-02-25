from django.http.response import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
)
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django_q.tasks import async_task
from users.tokens import user_tokenizer, password_reset_tokenizer
from django.utils.translation import gettext as _
from django.contrib import messages
from .forms import LoginForm, ResetRequestForm, ResetPassowrdForm

User = get_user_model()


def login_view(request):
    """Primary entrypoint login view

    Args:
        request ([type]): [description]
    """
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=str(username), password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, _("Wrong username or password"))
                return redirect("login")
        else:
            messages.error(request, _("Wrong credentials"))
            return redirect("login")

    if request.method == "GET":
        return render(request, "users/login.html")


def thermostat_login_view(request):
    """Primary entrypoint login view

    Args:
        request ([type]): [description]
    """
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=str(username), password=password)
            if user is not None:
                login(request, user)
                return redirect("thermostat-control")
            else:
                messages.error(request, _("Wrong username or password"))
                return redirect("login")
        else:
            messages.error(request, _("Wrong credentials"))
            return redirect("login")

    if request.method == "GET":
        return render(request, "thermostat/login.html")


@login_required(login_url="thermostat-login")
def thermostat_control_view(request):

    if request.method == "GET":
        template = "thermostat/panel.html"
        return render(request, template)

    return HttpResponseForbidden()


def thermostat_logout_view(request):
    if request.method == "GET":
        logout(request)
        messages.success(
            request, _("You've been successfully logged out. See you soon!")
        )
        return redirect("thermostat-login")


def logout_view(request):
    if request.method == "GET":
        logout(request)
        messages.success(
            request, _("You've been successfully logged out. See you soon!")
        )
        return redirect("login")


def guest_token_validation(request, user_id, token):

    user_id = force_str(urlsafe_base64_decode(user_id))
    try:
        user = User.objects.get(pk=user_id)
    except:
        return HttpResponseNotAllowed
    if user and user_tokenizer.check_token(user, token):
        print(
            "user_tokenizer.check_token(user, token)",
            user_tokenizer.check_token(user, token),
        )
        login(request, user)
        return redirect("dashboard")
    else:
        return HttpResponse("Link expired or broken")


@login_required(login_url="login")
def restricted_area_view(request):

    if request.method == "GET":
        template = "dashboard/panel.html"

        return render(request, template)

    return HttpResponseForbidden()


def request_password_reset(request):
    """Simple view that Allows user
    to request password reset link
    """

    template = "users/request_reset.html"

    if request.method == "GET":
        return render(request, template)

    if request.method == "POST":
        form = ResetRequestForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username)
        except:
            messages.info(
                request,
                _("We couldn't find this email address. Please, check you input."),
            )
            return redirect("request-reset")

        # user found, sendind password reset link
        async_task("users.utils.send_password_reset_link", user.pk)
        messages.success(
            request,
            "We've sent a message to your email. Please, follow instructions to reset your account password",
        )
        return redirect("request-reset")


def validate_password_reset_token(request, user_id, token):

    user_id = force_str(urlsafe_base64_decode(user_id))
    try:
        user = User.objects.get(pk=user_id)
    except:
        return HttpResponse("Security link has expired or broken")
    if user and password_reset_tokenizer.check_token(user, token):
        login(request, user)
        return redirect("new-password")
    else:
        return HttpResponse("Security link has expired or broken")


@login_required(login_url="login")
def save_new_password(request):

    template = "users/new_password.html"
    if request.method == "GET":
        return render(request, template)

    if request.method == "POST":
        form = ResetPassowrdForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            password1 = form.cleaned_data.get("password1")

            print("User", request.user)
            print("password", password)
            print("password1", password1)
            if password != password1:
                messages.warning(
                    request,
                    "Passwords aren't the same. Please check your fields and try again.",
                )
                return redirect("new-password")

            user = request.user
            user.set_password(password)
            user.save()
            logout(request)
            messages.info(
                request,
                "Your password was successfully changed. Please, login to your account",
            )
            return redirect("login")
