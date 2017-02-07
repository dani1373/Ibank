from __future__ import unicode_literals

from django.db import models

from bank.models import Branch
from customer.models import Account
from employee.models import Employee


class ATM(models.Model):
    branch = models.ForeignKey(Branch)

    minimum = models.PositiveIntegerField(default=0, null=False)

    def satisfy(self, amount):
        money_list = []
        for atm_money in self.atmmoney_set.all():
            money_list.append((atm_money.money.amount, atm_money.count))

        sorted_money_list = sorted(money_list, reverse=True)
        current_amount = amount
        solution = []
        for money, count in sorted_money_list:
            total = 0
            while current_amount > 0:
                if money <= current_amount and total + 1 <= count:
                    total += 1
                    current_amount -= money
                else:
                    break
            if total > 0:
                solution.append((money, total))

        if current_amount == 0:
            return True, solution
        else:
            return False, []


# just for stats
class AddMoney(models.Model):
    atm = models.ForeignKey(ATM)

    employee = models.ForeignKey(Employee)

    amount = models.PositiveIntegerField(null=False, blank=False, db_index=True)
    count = models.PositiveIntegerField(null=False, blank=False, db_index=True)


class Money(models.Model):
    amount = models.PositiveIntegerField(unique=True, null=False, blank=False, db_index=True)


class Card(models.Model):
    account = models.ForeignKey(Account)

    pin = models.CharField(max_length=4, null=False, blank=False, default='0000')
    card_number = models.CharField(max_length=16, null=False, blank=False, unique=True, db_index=True)


class ATMMoney(models.Model):
    money = models.ForeignKey(Money)
    count = models.PositiveIntegerField(null=False, default=0)
    atm = models.ForeignKey(ATM)
