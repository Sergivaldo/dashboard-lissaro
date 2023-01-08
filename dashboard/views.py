from django.shortcuts import render

from dashboard.service.api import api


# BASE_API_URL = "https://bling.com.br/b/Api/v2/"
# PAYMENT_ENDPOINT = "contaspagar"
# RECEIVEMET_ENDPOINT = "contasreceber"
# API_KEY = "9f8434c5983423bbed5130d60e42b3aabd01017f26041e01af4341545646db337fd2a73f"
def home(request):
    BASE_API_URL = "https://bling.com.br/b/Api/v2/"
    PAYMENT_ENDPOINT = "contaspagar"
    RECEIVEMET_ENDPOINT = "contasreceber"
    API_KEY = "9f8434c5983423bbed5130d60e42b3aabd01017f26041e01af4341545646db337fd2a73f"
    payments = api.Api(base_url=BASE_API_URL,
                       endpoint=PAYMENT_ENDPOINT, apikey=API_KEY)
    return render(request, 'dashboard/pages/index.html', context={
        'payment_bills_today': payments.get_bills_today(),
        'payment_bills_rest': payments.get_bills_rest(),
        'payment_bills_late': payments.get_late_bills(),
        'payment_value_today': payments.get_total_value_today(),
        'payment_value_rest': payments.get_total_value_rest(),
        'payment_value_late': payments.get_total_value_late()})
