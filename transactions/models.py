from django.db import models


# Create your models here.
class Transaction(models.Model):
    date = models.DateField()
    country = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    net = models.DecimalField(max_digits=8, decimal_places=2)
    converted_net = models.DecimalField(max_digits=8,
                                        decimal_places=2)  # Added because of unclear conversion instruction
    vat = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.transaction_type} '
