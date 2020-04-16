from .models import *
from celery import shared_task
from .models import *

@shared_task
def process_operation(amount, client, operation):
    user = Client.objects.get(id=client)
    if operation == 'addition':
        user.balance += int(amount)
        user.save()


    elif operation == 'substraction':
        user.hold += int(amount)
        user.save()

@shared_task
def process_hold():
    clients = Client.objects.filter(hold__gt=0, balance__gt=0, status=True)
    for client in clients:
        if client.balance >= client.hold:
            client.balance -= client.hold
            client.hold = 0
        else:
            amount = client.balance
            client.hold -= client.balance
            client.balance = 0
        client.save()

    print('Processed {} accounts'.format(len(clients)))