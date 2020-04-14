from .models import *
from celery import shared_task

@shared_task
def process_operation(amount, user, operation):
    if operation == 'addition':
        user.balance += amount
        user.save()

    elif operation == 'substraction':
        user.hold -= amount
        user.save()

    elif operation == 'on_hold':
        user.hold += amount
        user.balance -= amount
        user.save()
        process_operation.apply_async((amount, user, 'substraction'), countdown=40)