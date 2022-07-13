from django.urls import path

from transactions.api.views import TransactionAPIListView, TransactionCreateApiView

urlpatterns = [
    path('retrieveRows/', TransactionAPIListView.as_view(), name='retrieve-rows'),
    path('processFile/', TransactionCreateApiView.as_view(), name='process-file'),
]
