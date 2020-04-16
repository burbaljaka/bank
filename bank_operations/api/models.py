from django.db import models
import uuid

# Create your models here.
class Client(models.Model):

    OPENED = True
    CLOSED = False
    STATUS_CHOICES = [
        (OPENED, 'Opened'),
        (CLOSED, 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=200)
    balance = models.PositiveIntegerField()
    hold = models.PositiveIntegerField()
    status = models.BooleanField(choices=STATUS_CHOICES, default=OPENED)

    def __str__(self):
        return str(self.id)


# class Transaction(models.Model):
#     ADD = 'a'
#     SUBSTRACT = 's'
#     OPERATION_CHOICES = [
#         (ADD, 'Add'),
#         (SUBSTRACT, 'Substract'),
#     ]
#     date_created = models.DateTimeField(auto_now_add=True)
#     amount = models.PositiveIntegerField()
#     operation = models.CharField(max_length=1, choices=OPERATION_CHOICES)
#     user = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
#     OPENED = True
#     CLOSED = False
#     STATUS_CHOICES = [
#         (OPENED, 'Opened'),
#         (CLOSED, 'Closed'),
#     ]
#     status = models.BooleanField(choices=STATUS_CHOICES)