from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .tasks import *
from .serializers import *

def make_response(status=status.HTTP_400_BAD_REQUEST,
                  result=False,
                  operation='ping',
                  amount=None,
                  user=None,
                  description='Unknown issue'):

    operation_data = None if user==None else {
        'uuid': user.id,
        'name': user.name,
        'client_status': user.status,
        'operation': operation,
        'amount': amount,
        'balance': user.balance,
        'hold': user.hold
    }

    return {'status':status,
            'result': result,
            'addition': operation_data,
            'description': description
            }
0

# Create your views here.
@api_view(['POST'])
def addition(request):
    operation = 'addition'
    serializer = OperationSerializer(data=request.data)
    serializer.is_valid()

    if serializer.errors:
        return Response(make_response(description='Please provide correct data', operation=operation), status=status.HTTP_400_BAD_REQUEST)
    try:
        user = Client.objects.get(id=serializer.validated_data['id'])
    except:
        return Response(make_response(description='Incorrect user id', operation=operation, status=status.HTTP_400_BAD_REQUEST))

    if not user.status:
        return Response(make_response(description='Client account is closed', operation=operation, user=user), status=status.HTTP_400_BAD_REQUEST)

    amount = serializer.validated_data['amount']
    operate = 'addition'
    process_operation.delay(amount, user.id, operate)

    return Response(make_response(status=status.HTTP_200_OK,
                                  result=True,
                                  operation=operate,
                                  amount=amount,
                                  user=user,
                                  description='Accepted'))


@api_view(['POST'])
def substraction(request):
    operation='substraction'

    serializer = OperationSerializer(data=request.data)
    serializer.is_valid()
    if serializer.errors:
        return Response(make_response(description='Please provide correct data', operation=operation),
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Client.objects.get(id=serializer.validated_data['id'])
    except:
        return Response(make_response(description='Incorrect user id', operation=operation),
                        status=status.HTTP_400_BAD_REQUEST)

    if not user.status:
        return Response(make_response(description='Client account is closed', operation=operation, user=user),
                        status=status.HTTP_400_BAD_REQUEST)

    amount = serializer.validated_data['amount']
    if user.balance < user.hold + int(amount):
        return Response(make_response(description='You do not have enough balance to process such operation'),
                        status=status.HTTP_400_BAD_REQUEST)

    operate = 'substraction'
    count = 10
    process_operation.delay(amount, user.id, operate)
    return Response(make_response(status=status.HTTP_200_OK,
                                  result=True,
                                  operation='substraction',
                                  amount=amount,
                                  user=user,
                                  description='Accepted'))

@api_view(['GET'])
def test(request):
    return Response(make_response(status=status.HTTP_200_OK,
                                  description='Service is up currently',
                                  result=True))


@api_view(['POST'])
def get_status(request):
    if 'id' in request.data:
        try:
            user = Client.objects.get(id=request.data['id'])
        except:
            return Response(make_response(description='Please provide valid id', operation='get_status'))
    else:
        return Response(make_response(description='Please provide valid id', operation='get_status'))

    return Response(make_response(description='Client account info',
                                  user=user,
                                  operation='get_status',
                                  status=status.HTTP_200_OK,
                                  result=True))