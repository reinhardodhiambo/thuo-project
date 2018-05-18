import hashlib
import pickle

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from vehicle_transfer.models import Owner

from vehicle_transfer.models import Details


# from vehicle_transfer_confirmation.models import Status

# # Confirm Vehicle Transfer
# @api_view(http_method_names=['POST'])
# @renderer_classes((JSONRenderer,))
# def carTransferConfirmation(request):
#     car_transfer_edit = Owner.objects.get(transfer_id=request.data['transfer'])
#
#     transfer_confirm = Status(transfer_id=car_transfer_edit.transfer_id, fullname=request.data['name'], national_id=request.data['national'],
#                               mobile=request.data['mobile'],dob=request.data['dob'], pin=request.data['pin'],
#                               email=request.data['email'], reg_id=request.data['reg'],
#                               vehicle_type=request.data['type'], make=request.data['make'],
#                               vehicle_model=request.data['model'], previous_owner_name=request.data['p_name'],
#                               previous_owner_mobile=request.data['p_mobile'], previous_owner_email=request.data['p_email'])
#
#     if car_transfer_edit:
#         car_transfer_edit.vehicle_status = 1
#     #car_transfer_edit.save()
#
#     if transfer_confirm and car_transfer_edit:
#         transfer_confirm.save()
#         car_transfer_edit.save()
#         response = {'transfer_id': transfer_confirm.transfer_id,  'name': transfer_confirm.fullname, 'national': transfer_confirm.national_id, 'mobile': transfer_confirm.mobile, 'dob': transfer_confirm.dob,
#                     'pin': transfer_confirm.pin, 'email': transfer_confirm.email, 'reg_no': transfer_confirm.reg_id, 'type': transfer_confirm.vehicle_type,
#                     'make': transfer_confirm.make, 'model': transfer_confirm.vehicle_model}
#         pickle.dumps(response)
#         m = hashlib.sha3_256()
#         m.update(pickle.dumps(response))
#         m.digest()
#         m.hexdigest()
#         response2 = {'name': transfer_confirm.fullname, 'national': transfer_confirm.national_id, 'mobile': transfer_confirm.mobile, 'dob': transfer_confirm.dob,
#                     'pin': transfer_confirm.pin, 'email': transfer_confirm.email, 'reg_no': transfer_confirm.reg_id, 'type': transfer_confirm.vehicle_type,
#                     'make': transfer_confirm.make, 'model': transfer_confirm.vehicle_model, 'previous_owner_name': transfer_confirm.previous_owner_name,
#                     'previous_owner_mobile': transfer_confirm.previous_owner_mobile, 'previous_owner_email': transfer_confirm.previous_owner_email,
#                     'last_block': m.hexdigest(), 'nonce': 0}
#
#         return Response(response2)
#     return Response(status=status.HTTP_400_BAD_REQUEST)

# Launch Page
def carConfirmation(request, user):
    vehicles = Details.objects.filter(national_id=user, vehicle_status=0).values()
    return render(request, 'car_reg/vehicle_transfer_confirmation_status.html', {'vehicles': vehicles})


# Car Owner View
def carConfirmationView(request,transfer):
    vehicle = Details.objects.get(transfer_id=transfer)
    return render(request, 'car_reg/vehicle_transfer_confirmation_status_view.html', {'vehicle': vehicle})
