from datetime import datetime

from rest_framework.generics import ListAPIView, CreateAPIView

from transactions.models import Transaction
from transactions.utils import parse_csv, save_csv, get_country_full_name
from .serializer import TransactionSerializer


class TransactionCreateApiView(CreateAPIView):
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        file = self.request.FILES.get('file')
        data = parse_csv(file)
        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return save_csv(serializer)


class TransactionAPIListView(ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        data = Transaction.objects.all()
        country = self.request.query_params.get('country')
        date = self.request.query_params.get('date')
        if country:
            country_name = get_country_full_name(country)
            if data.filter(country=country).exists():
                data = data.filter(country=country)
            elif data.filter(country=country).exists():
                data = data.filter(country=country_name)
            else:
                return data.filter(country=country_name)
        if date:
            new_date = datetime.strptime(date, '%Y/%m/%d').strftime("%Y-%m-%d")
            data = data.filter(date=new_date)
        return data
