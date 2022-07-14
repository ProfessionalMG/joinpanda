import codecs
import csv
import time
from datetime import datetime

import requests
from _datetime import timedelta
from rest_framework.response import Response

from joinpanda.settings import COUNTRY_LAYER_API_KEY
from transactions.models import Transaction


# TODO:Write Tests
# TODO: Add converted currency to model
def change_currency(currency, amount):
    ecb_url = f'https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.{currency}.EUR.SP00.A'
    today = datetime.today().date()
    params = {
        'startPeriod': today - timedelta(days=100),
        'endPeriod': today,
        'format': 'jsondata',
        'detail': 'dataonly'
    }
    api_call = requests.get(ecb_url, params).json()
    data_sets = api_call['dataSets'][0]['series']['0:0:0:0:0']['observations']
    last_item = list(data_sets.keys())[-1]
    ex_rate = data_sets[last_item][0]
    converted_amount = amount / ex_rate

    return round(converted_amount, 2)


def parse_csv(file):
    reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
    data = []
    for read in reader:
        read['Date'] = datetime.strptime(read['Date'], '%Y/%m/%d').strftime("%Y-%m-%d")
        # TODO: Check that dates added to the dict are only 2020
        new_dict = {
            'date': read['Date'],
            'transaction_type': read['Purchase/Sale'],
            'country': read['Country'],
            'currency': read['Currency'],
            'net': read['Net'],
            # 'converted_net':'something',#TODO:Convert so that its in euros
            'vat': read['VAT']
        }
        data.append(new_dict)
    return data


def save_csv(serializer):
    transaction_list = []
    for row in serializer.data:
        transaction_list.append(
            Transaction(
                date=row['date'],
                country=row['country'],
                transaction_type=row['transaction_type'],
                currency=row['currency'],
                net=row['net'],
                vat=row['vat'],
            )
        )
    Transaction.objects.bulk_create(transaction_list)
    return Response('Data Uploaded Successfully')


def get_country_full_name(country):
    params = {'access_key': COUNTRY_LAYER_API_KEY, }
    country_endpoint = f'http://api.countrylayer.com/v2/alpha/{country}'
    api_call = requests.get(country_endpoint, params).json()
    country_name = api_call['name']
    time.sleep(1)
    return country_name
