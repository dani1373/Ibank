from django_cron import CronJobBase, Schedule

from ibank.mailhandler import sendMail
from service.views import periodic_order_resolver
from transaction.views import notify_customer


class PeriodicResolver(CronJobBase):
    RUN_EVERY_MINS = 24*60

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ibank.periodicresolver'

    def do(self):
        periodic_order_resolver()

class MailNotifier(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ibank.mailnotifier'

    def do(self):
        notify_customer()
