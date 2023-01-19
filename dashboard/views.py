import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

import dashboard.utils.rsa_encript as rsa
from dashboard.forms import LoginForm, RegisterForm
from dashboard.service.api import api
from dashboard.service.api.api_constants import (BASE_API_URL,
                                                 PAYMENT_ENDPOINT,
                                                 RECEIVEMET_ENDPOINT)
from dashboard.service.robot.bling_client import get_accounts

from .models import ApiData, BlingUser, Keys, User


@login_required(login_url="dashboard:login")
def dashboard(request):
    user = User.objects.filter(username=request.user.username).first()
    bling_user = BlingUser.objects.filter(
        dashboard_user=user.pk).first()

    if bling_user is not None:
        private_key = rsa.get_private_key(bling_user.keys.private_key)
        original_password = rsa.decrypt(bling_user.password, private_key)
        form = RegisterForm(
            initial={'user_name': bling_user.user_name, 'password': original_password, 'api_key': bling_user.api_key})

        if bling_user.api_data is not None:
            payments = json.loads(bling_user.api_data.payments)
            receivements = json.loads(bling_user.api_data.receivements)
            bank_accounts = json.loads(bling_user.api_data.bank_accounts)
            updated_at = datetime.strftime(
                bling_user.api_data.updated_at, "%d/%m/%Y, %H:%M:%S")
        else:
            return render(request, 'dashboard/pages/index.html', context={
                'form': form})

        return render(request, 'dashboard/pages/index.html', context={
            'form': form,
            'total_balance': bank_accounts['total_balance'],
            'balances_on_account': bank_accounts['balances_on_account'],
            'payment_bills_today': payments['payment_bills_today'],
            'payment_bills_rest': payments['payment_bills_rest'],
            'payment_bills_late': payments['payment_bills_late'],
            'payment_value_today': payments['payment_value_today'],
            'payment_value_rest': payments['payment_value_rest'],
            'payment_value_late': payments['payment_value_late'],
            'receivements_value_today': receivements['receivements_value_today'],
            'receivements_value_rest': receivements['receivements_value_rest'],
            'receivements_value_late': receivements['receivements_value_late'],
            'updated_at': updated_at}
        )

    else:
        form = RegisterForm()
        return render(request, 'dashboard/pages/index.html', context={
            'form': form})


@ login_required(login_url="dashboard:login")
def register_bling_user(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = User.objects.filter(username=request.user.username).first()
        bling_user = BlingUser.objects.filter(
            dashboard_user=user.pk).first()
        if bling_user is not None:
            bling_user.api_key = form.cleaned_data.get("api_key")
            bling_user.user_name = form.cleaned_data.get("user_name")

            public_key = rsa.get_public_key(bling_user.keys.public_key)
            bling_user.password = rsa.encrypt(
                form.cleaned_data.get("password"), public_key)

        else:
            (public_key, private_key) = rsa.generate_keys()
            keys = Keys.objects.create(
                public_key=rsa.save_public_key(public_key),
                private_key=rsa.save_private_key(private_key)
            )
            bling_user = BlingUser.objects.create(
                user_name=form.cleaned_data.get("user_name"),
                password=rsa.encrypt(form.cleaned_data.get(
                    "password"), public_key),
                api_key=form.cleaned_data.get("api_key"),
                dashboard_user=user,
                keys=keys
            )

        bling_user.save()
        messages.success(request, 'Dados de usuário registrados')
    else:
        messages.error(request, 'Erro ao registrar dados')
    return redirect(reverse("dashboard:main"))


def get_data(request):
    user = User.objects.filter(username=request.user.username).first()

    try:
        bling_user = BlingUser.objects.filter(
            dashboard_user=user.pk).first()
        API_KEY = bling_user.api_key
    except Exception:
        messages.error(
            request, 'Registre um usuário do bling antes de buscar os dados')
        return redirect(reverse("dashboard:main"))

    try:
        payments = api.Api(base_url=BASE_API_URL,
                           endpoint=PAYMENT_ENDPOINT, apikey=API_KEY)
        receivements = api.Api(base_url=BASE_API_URL,
                               endpoint=RECEIVEMET_ENDPOINT, apikey=API_KEY)
    except Exception as e:
        messages.error(request, f'Bling API: {e.args[0]}')
        return redirect(reverse("dashboard:main"))
    payments = {
        'payment_bills_today': payments.get_bills_today(),
        'payment_bills_rest': payments.get_bills_rest(),
        'payment_bills_late': payments.get_late_bills(),
        'payment_value_today': payments.get_total_value_today(),
        'payment_value_rest': payments.get_total_value_rest(),
        'payment_value_late': payments.get_total_value_late(),
    }

    receivements = {
        'receivements_value_today': receivements.get_total_value_today(),
        'receivements_value_rest': receivements.get_total_value_rest(),
        'receivements_value_late': receivements.get_total_value_late()
    }

    try:
        private_key = rsa.get_private_key(bling_user.keys.private_key)
        original_password = rsa.decrypt(bling_user.password, private_key)
        bank_accounts = get_accounts(
            username=bling_user.user_name, password=original_password)
    except Exception as e:
        messages.error(
            request, e.args[0])
        return redirect(reverse("dashboard:main"))

    if bling_user.api_data is None:

        bling_user.api_data = ApiData.objects.create(
            payments=json.dumps(payments),
            receivements=json.dumps(receivements),
            bank_accounts=json.dumps(bank_accounts),
            updated_at=datetime.now(
                ZoneInfo('America/Bahia')) + timedelta(hours=-3)
        )
    else:
        bling_user.api_data.payments = json.dumps(payments)
        bling_user.api_data.receivements = json.dumps(receivements)
        bling_user.api_data.bank_accounts = json.dumps(
            bank_accounts)
        bling_user.api_data.updated_at = datetime.now(
            ZoneInfo('America/Bahia')) + timedelta(hours=-3)

    bling_user.save()
    messages.success(request, "Dados atualizados")
    return redirect(reverse('dashboard:main'))


def login_view(request):
    form = LoginForm()
    return render(request, 'dashboard/pages/login.html', {
        'form': form,
        'form_action': reverse('dashboard:check')
    })


def redirect_login(request):
    return redirect(reverse("dashboard:login"))


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
        else:
            messages.error(request, 'Usuário não encontrado')
    else:
        messages.error(request, 'Credenciais inválidas')
    return redirect(reverse("dashboard:main"))


@ login_required(login_url="dashboard:login")
def logout_view(request):
    logout(request)
    return redirect(reverse("dashboard:login"))
