# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clients(models.Model):
    limits = models.IntegerField()
    initial_balance = models.IntegerField()
    actual_balance = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'clients'
        verbose_name = 'client'
        verbose_name_plural = 'clients'


class Transactions(models.Model):
    value = models.IntegerField()
    transaction_type = models.CharField()
    description = models.CharField(max_length=10)
    completed_at = models.DateTimeField()
    client = models.ForeignKey(Clients, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'transactions'
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
