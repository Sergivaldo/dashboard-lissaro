from datetime import datetime

import pytz
import requests


class Api:

    def __init__(self, base_url, endpoint, apikey):
        self.base_url = base_url
        self.url_endpoint = endpoint
        self.apikey = apikey
        self.url = f'{self.base_url}{self.url_endpoint}/json&apikey={self.apikey}'
        self.obj_item_name = self.__set_obj_item_name(self.url_endpoint)
        self.data = self.__get_pendent_bills(self.url, endpoint)
        self.__sort_by_due_date(self.url_endpoint)

    # Faz uma requisição a api retornando um json com os dados.
    def __fetch_api(self, url, endpoint) -> list:
        response = requests.get(url)
        data = response.json()['retorno'][endpoint]
        return data

    # Ordena os dados por data de vencimento
    def __sort_by_due_date(self, endpoint) -> None:
        self.data.sort(
            key=lambda item: item[self.obj_item_name]['vencimento'])

    # Busca na api todas as contas pendentes
    def __get_pendent_bills(self, url, endpoint):
        data = self.__fetch_api(url, endpoint)
        pendent_bills = list()
        for bill in data:
            if bill[self.obj_item_name]['situacao'] == 'aberto' or bill[
                    self.obj_item_name]['situacao'] == 'parcial':

                bill[self.obj_item_name]['atrasado'] = self.__is_late_bill(
                    bill)
                pendent_bills.append(bill)

        return pendent_bills

    # Compara se a data de vencimento da conta é maior, menor ou igual.
    def __compare_dates(self, bill) -> int:
        current_date = datetime.now(pytz.timezone('America/Bahia')).date()
        due_date_bill = datetime.strptime(
            bill[self.obj_item_name]['vencimento'], '%Y-%m-%d').date()

        if due_date_bill > current_date:
            return 1
        elif due_date_bill == current_date:
            return 0
        else:
            return -1

    # Compara se o mês de vencimento da conta é maior, menor ou igual.
    def __compare_months(self, bill):
        current_month = datetime.now(
            pytz.timezone('America/Bahia')).date().month
        due_month_bill = datetime.strptime(
            bill[self.obj_item_name]['vencimento'], '%Y-%m-%d').date().month

        if due_month_bill > current_month:
            return 1
        elif due_month_bill == current_month:
            return 0
        else:
            return -1

    # Verifica se o pagamento está atrasado
    def __is_late_bill(self, bill):

        if (self.__compare_dates(bill) == 0
                or self.__compare_dates(bill) == 1):
            return 'false'
        return 'true'

    # Verifica qual o endpoint e seta qual será o nome dos itens do objeto
    def __set_obj_item_name(self, endpoint):
        if endpoint == 'contaspagar':
            return 'contapagar'
        else:
            return 'contaReceber'

    # Pega todas as contas referente ao dia atual
    def get_bills_today(self):
        bills_today = list()
        for bill in self.data:
            if (self.__compare_dates(bill) == 0):
                bills_today.append(bill)

        return bills_today

    # Pega todas as contas do restante do mês
    def get_bills_rest(self):
        bills_rest = list()
        for bill in self.data:
            if (self.__compare_dates(bill) == 1):
                bills_rest.append(bill)

        return bills_rest

    # Pega o valor total referente ao dia atual
    def get_total_value_today(self):
        total_value = 0.0
        for bill in self.data:
            if self.__compare_dates(bill) == 0:
                total_value += float(bill[self.obj_item_name]['valor'])

        return total_value

    # Pega o valor total referente ao mês
    def get_total_value_rest(self):
        total_value = 0.0
        for bill in self.data:
            if (self.__compare_dates(bill) == 1
                    and self.__compare_months(bill) == 0):
                total_value += float(bill[self.obj_item_name]['valor'])

        return total_value

    # Pega o valor total de todas as contas atrasadas
    def get_total_value_late(self):
        total_value = 0.0
        for bill in self.data:
            if bill[self.obj_item_name]['atrasado'] == 'true':
                total_value += float(bill[self.obj_item_name]['valor'])

        return total_value

    def get_late_bills(self):
        late_bills = list()
        for bill in self.data:
            if bill[self.obj_item_name]['atrasado'] == 'true':
                late_bills.append(bill)

        return late_bills

    # Recarrega os dados colhidos da api fazendo uma nova requisição
    def refresh(self) -> None:
        self.data = self.__get_pendent_bills(self.url, self.url_endpoint)
        self.__sort_by_due_date(self.url_endpoint)

    @property
    def printData(self):
        print(self.data)

BASE_API_URL = "https://bling.com.br/b/Api/v2/"
PAYMENT_ENDPOINT = "contaspagar"
RECEIVEMET_ENDPOINT = "contasreceber"
API_KEY = "9f8434c5983423bbed5130d60e42b3aabd01017f26041e01af4341545646db337fd2a73f"

a = Api(BASE_API_URL, PAYMENT_ENDPOINT, API_KEY)

print(a.get_late_bills())