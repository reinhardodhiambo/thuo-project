import hashlib
import pickle

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from vehicle_transfer.models import Owner
import vehicle_registration.views
from django.http import HttpRequest

# Transfer Vehicle
@api_view(http_method_names=['POST'])
@renderer_classes((JSONRenderer,))
def carTransfer(request):

    car_transfer = Owner(fullname=request.data['name'], national_id=request.data['national'], mobile=request.data['mobile'],
                      dob=request.data['dob'], pin=request.data['pin'],
                      email=request.data['email'], reg_id=request.data['reg'],
                      vehicle_type=request.data['type'], make=request.data['make'],
                      vehicle_model=request.data['model'], previous_owner_name=request.data['p_name'],
                      previous_owner_mobile=request.data['p_mobile'], previous_owner_email=request.data['p_email'],
                      vehicle_status=0)

    if car_transfer:
        car_transfer.save()
        response = {'name': car_transfer.fullname, 'national': car_transfer.national_id, 'mobile': car_transfer.mobile, 'dob': car_transfer.dob,
                    'pin': car_transfer.pin, 'email': car_transfer.email, 'reg_no': car_transfer.reg_id, 'type': car_transfer.vehicle_type,
                    'make': car_transfer.make, 'model': car_transfer.vehicle_model}
        pickle.dumps(response)
        n = hashlib.sha3_256()
        n.update(pickle.dumps(response))
        n.digest()
        n.hexdigest()
        fake_request =HttpRequest()
        car_r = vehicle_registration.views.carRegistration(fake_request)
        print(car_r)
        response2 = {'name': car_transfer.fullname, 'national': car_transfer.national_id, 'mobile': car_transfer.mobile, 'dob': car_transfer.dob,
                    'pin': car_transfer.pin, 'email': car_transfer.email, 'reg_no': car_transfer.reg_id, 'type': car_transfer.vehicle_type,
                    'make': car_transfer.make, 'model': car_transfer.vehicle_model, 'previous_owner_name': car_transfer.previous_owner_name,
                    'previous_owner_mobile': car_transfer.previous_owner_mobile, 'previous_owner_email': car_transfer.previous_owner_email,
                    'vehicle_status': car_transfer.vehicle_status, 'last_block': n.hexdigest(), 'nonce': 0}
        return Response(response2)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# Launch Page
def carOwner(request):
    return render(request, 'car_reg/vehicle_transfer_owner.html')

# Car Owner View
def carOwnerView(request):
    return render(request, 'car_reg/vehicle_transfer_owner_view.html')